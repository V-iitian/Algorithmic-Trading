import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
import datetime as dt

start = dt.datetime(2024, 1, 1)
end = dt.datetime(2025, 5, 1)


def RSI(start, end, ticker):
    df = yf.download(ticker, start, end)
    df.columns = df.columns.droplevel(1)
    df['DIFF'] = df['Close']-df['Close'].shift(1)
    df['DIFF'].fillna(0)
    conditions = [(df['DIFF'] >= 0), (df['DIFF'] < 0)]
    choices_gain = [df['DIFF'], 0]
    choices_loss = [0, -1*df['DIFF']]
    df['GAIN'] = np.select(conditions, choices_gain, default=0.0)
    df['LOSS'] = np.select(conditions, choices_loss, default=0.0)
    df['GAIN_AVG'] = df['GAIN'].rolling(window=14).mean()
    df['LOSS_AVG'] = df['LOSS'].rolling(window=14).mean()
    df['RS'] = df['GAIN_AVG']/df['LOSS_AVG']
    df['RSI'] = 100-(100/(1+df['RS']))
    df.drop(columns=['GAIN', 'LOSS', 'GAIN_AVG',
            'LOSS_AVG', 'RS'], inplace=True)
    plt.subplot(211)
    plt.plot(df['Close'], 'r-', label='CLOSE_PRICE')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Close')
    plt.title('CLOSE')
    plt.subplot(212)
    plt.plot(df['RSI'], 'b-', label='RSI')
    plt.axhline(y=30, color='red', linestyle='--',
                linewidth=1.5, label="higher_threshold")
    plt.axhline(y=70, color='red', linestyle='--',
                linewidth=1.5, label="Lower_threshold")
    plt.legend(loc="upper left")
    plt.ylabel('RSI')
    plt.ylim(0, 100)
    plt.title('RSI')
    plt.tight_layout(pad=2.0)
    my_lines = [mpf.make_addplot(df['RSI'], color='fuchsia', width=1.5)]
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


RSI(start, end, "RELIANCE.NS")
