import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import datetime as dt
start = dt.datetime(2026, 6, 1)
end = dt.datetime(2026, 6, 5)


def VWAP(ticker, start, end):
    df = yf.download(ticker, start, end, interval='5m')
    df.columns = df.columns.droplevel(1)
    df['Total Volume'] = df['Volume'].cumsum()
    df['Typical Price'] = (df['High']+df['Low']+df['Close'])/3
    df['VP'] = df['Typical Price']*df['Volume']
    df['Total VP'] = df['VP'].cumsum()
    df['VWAP'] = df['Total VP']/df['Total Volume']
    fig, ax1 = plt.subplots()
    ax1.plot(df['Close'], ms=2.0, label='Close Price')
    ax1.plot(df['Close'], 'ro')
    plt.legend(loc='upper left')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price')
    ax2 = ax1.twinx()
    ax2.plot(df['VWAP'], 'g', lw=1.5, ms=10, label='VWAP')
    ax2.plot(df['VWAP'], 'bo')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('VWAP')
    plt.title('Volume Indicator')
    my_colors = mpf.make_marketcolors(
        up='green',
        down='red',
        edge='black',
        wick='black',
        volume='Blue'  # Optional: Color for the volume bars
    )
    my_style = mpf.make_mpf_style(
        base_mpf_style='yahoo', marketcolors=my_colors)

    mpf.plot(df, type='candle', volume=True, style=my_style)


VWAP("RELIANCE.NS", start, end)
