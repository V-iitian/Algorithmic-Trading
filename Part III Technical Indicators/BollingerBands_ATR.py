import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
import datetime as dt

start = dt.datetime(2024, 1, 1)
end = dt.datetime(2024, 12, 1)


def Bollinger_ATR(start, end, ticker):

    # Downloadig the data set

    df = yf.download(ticker, start, end)
    df.columns = df.columns.droplevel(1)

    # TR Calculations
    df['H-L'] = df['High']-df['Low']
    df['L-Cp'] = abs(df['Low']-(df['Close'].shift(1)))
    df['H-Cp'] = abs(df['High']-(df['Close'].shift(1)))
    conditions = [(df['H-L'] >= df['L-Cp']) & (df['H-L'] >= df['H-Cp']),
                  (df['H-L'] <= df['L-Cp']) & (df['L-Cp'] >= df['H-Cp']),
                  (df['H-L'] <= df['H-Cp']) & (df['L-Cp'] <= df['H-Cp'])]
    choices = [df['H-L'], df['H-Cp'], df['L-Cp']]
    df['TR'] = np.select(conditions, choices, default=0.0)
    df['SMA'] = df['Close'].rolling(20).mean()

    # ATR Calculations
    # i have calculated range taking close price as current price or price at which i traded then it will give me volatility of this day for this price
    df['+ATR'] = (df['TR'].rolling(window=20).mean())+df['Close']
    df['-ATR'] = -(df['TR'].rolling(window=20).mean())+df['Close']

    # Bollinger_Calculatios

    df['+2SD'] = df['SMA']+2*(df['Close'].rolling(window=20).std())
    df['-2SD'] = df['SMA']-2*(df['Close'].rolling(window=20).std())

    # line charts plots
    plt.plot(df['Close'], 'r-', lw=1.0, label='CLOSE_PRICE')
    plt.plot(df['SMA'], 'b-', lw=1.0, label='20_DAY_SMA')
    plt.plot(df['+2SD'], 'r--', lw=0.5, label='SMA+2SD')
    plt.plot(df['-2SD'], 'r--', lw=0.5, label='SMA-2SD')
    plt.plot(df['+ATR'], 'g--', lw=0.5, label='SMA+ATR')
    plt.plot(df['-ATR'], 'g--', lw=0.5, label='SMA-ATR')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('PRICE')
    plt.title('CLOSE_BOLLINGER_BANDS_ATR')

    # candlestick charts plots
    my_lines = [mpf.make_addplot(df['+2SD'], color='black', width=1.5, label='SMA+2SD'),
                mpf.make_addplot(df['-2SD'], color='black',
                                 width=1.5, label='SMA-2SD'),
                mpf.make_addplot(df['+ATR'], color='blue',
                                 width=1.5, label='SMA+ATR'),
                mpf.make_addplot(df['-ATR'], color='blue', width=1.5, label='SMA-ATR')]
    mpf.plot(
        df,
        type='candle',
        volume=True,
        mav=(20),
        show_nontrading=False,
        style='charles',
        addplot=my_lines,
        title='Price with Moving Averages',
        figsize=(12, 6)
    )


Bollinger_ATR(start, end, "RELIANCE.NS")
