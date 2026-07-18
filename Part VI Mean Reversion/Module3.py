import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import yfinance as yf
import datetime as dt

start = dt.datetime(2024,1,1)
end = dt.datetime(2026,7,7)

df_1 = yf.download('HDFCBANK.NS',start,end)
df_2 = yf.download('ICICIBANK.NS',start,end)

df_1.columns = df_1.columns.droplevel(1)
df_2.columns = df_2.columns.droplevel(1)

df = df_1.merge(df_2,on='Date')
df['spread'] = df_1['Close']-df_2['Close']

def calculate_half_life(spread):
    """
    Calculates the half-life of mean reversion using an AR(1) model.
    """
    spread_diff = spread.diff().dropna()
    spread_lag = spread.shift(1).dropna()
    spread_diff = spread_diff.loc[spread_lag.index]
    
    X = sm.add_constant(spread_lag)
    model = sm.OLS(spread_diff, X).fit()
    
    lam = model.params.iloc[1]
    
    if lam >= 0:
        print("Spread is diverging. Half-life is infinite.")
        return np.inf
        
    half_life = -np.log(2) / lam
    print(f"Rate of Reversion (Lambda): {lam:.4f}")
    print(f"Estimated Half-Life: {half_life:.2f} days")
    
    return half_life

# Simulated Execution:
hl = calculate_half_life(df['spread'])

def generate_signals(spread, half_life_days):
    """
    Generates vectorized trading signals avoiding look-ahead bias.
    """
    window = int(max(10, round(half_life_days)))
    
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    
    z_score = (spread - rolling_mean) / rolling_std
    
    signals = pd.DataFrame(index=z_score.index)
    signals['z_score'] = z_score.round(3)
    signals['positions'] = 0
    
    entry_threshold = 2.0
    exit_threshold = 0.0
    current_pos = 0
    
    for i in range(len(z_score)):
        z = z_score.iloc[i]
        if pd.isna(z): continue
            
        if z < -entry_threshold and current_pos == 0:
            current_pos = 1
        elif z > entry_threshold and current_pos == 0:
            current_pos = -1
        elif z >= exit_threshold and current_pos == 1:
            current_pos = 0
        elif z <= exit_threshold and current_pos == -1:
            current_pos = 0
            
        signals.iloc[i, signals.columns.get_loc('positions')] = current_pos
        
    print(signals.dropna().tail(7))
    return signals

generate_signals(df['spread'],hl)