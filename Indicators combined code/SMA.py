import pandas as pd
import yfinance as yf
import mplfinance as mpf
import datetime as dt
import matplotlib.pyplot as plt

start = dt.datetime(2026, 1, 1)
end = dt.datetime(2026, 5, 1)

def EMA(start, end, ticker):
    df = yf.download(ticker, start, end)
    df.columns = df.columns.droplevel(1)
    df['EMA'] = df['Close'].ewm(span=10, adjust=False).mean()
    fig, ax1 = plt.subplots()
    ax1.plot(df['Close'], label='Close Price')
    plt.legend(loc='upper left')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax2 = ax1.twinx()
    ax2.plot(df['EMA'], 'g', lw=1.5, label='10-day-EMA')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('10-day-EMA')
    plt.title('EMA')
    my_lines = [mpf.make_addplot(df['EMA'], color='fuchsia', width=1.5)]
    mpf.plot(
        df,
        type='candle',
        volume=True,
        show_nontrading=False,
        style='charles',
        addplot=my_lines,
        title='Price with Moving Averages',
        figsize=(12, 6)
    )


EMA(start, end, "INFY")
