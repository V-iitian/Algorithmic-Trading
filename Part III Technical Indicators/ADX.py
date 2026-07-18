import pandas as pd 
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt 

start = dt.datetime(2025,1,1)
end = dt.datetime(2026,1,1)


def ADX(start,end,ticker):
    df = yf.download(ticker,start,end)
    df.columns = df.columns.droplevel(1)


    # DM Calculation
    df['+DM']=df['High']-df['High'].shift(1)
    df['-DM']=df['Low'].shift(1)-df['Low']

    #TR  & ATR calculation taken from ATR code 
    df['H-L'] = df['High']-df['Low']
    df['L-Cp'] = abs(df['Low']-(df['Close'].shift(1)))
    df['H-Cp'] = abs(df['High']-(df['Close'].shift(1)))
    conditions = [(df['H-L'] >= df['L-Cp']) & (df['H-L'] >= df['H-Cp']),
                  (df['H-L'] <= df['L-Cp']) & (df['L-Cp'] >= df['H-Cp']),
                  (df['H-L'] <= df['H-Cp']) & (df['L-Cp'] <= df['H-Cp'])]
    choices = [df['H-L'], df['H-Cp'], df['L-Cp']]
    df['TR'] = np.select(conditions, choices, default=0.0)
    df['ATR']=df['TR'].rolling(14).mean()




ADX(start,end,"RELIANCE.NS")