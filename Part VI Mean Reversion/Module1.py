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

def analyze_pair(price_A, price_B):
    """
    Evaluates two asset series for cointegration.
    Returns the spread, hedge ratio, ADF p-value, and a boolean flag.
    """
    # Step 1: OLS Regression to find the Hedge Ratio (gamma)
    X = sm.add_constant(price_B)
    model = sm.OLS(price_A, X).fit()
    
    mu = model.params.iloc[0]
    gamma = model.params.iloc[1]
    
    # Step 2: Construct the Spread (Synthetic Asset)
    spread = price_A - (gamma * price_B) - mu
    
    # Step 3: Augmented Dickey-Fuller Test on the Spread
    adf_result = adfuller(spread, maxlag=1)
    p_value = adf_result[1]
    
    # Check against a 95% confidence interval
    is_cointegrated = p_value < 0.05
    
    print(f"Hedge Ratio (Gamma): {gamma:.3f}")
    print(f"Constant (Mu): {mu:.3f}")
    print(f"ADF Test p-value: {p_value:.4f}")
    print(f"Cointegration Status: {is_cointegrated}")
    
    return spread, gamma, p_value, is_cointegrated

# Simulated Execution:
analyze_pair(df_1['Close'], df_2['Close'])