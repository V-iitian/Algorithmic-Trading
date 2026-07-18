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