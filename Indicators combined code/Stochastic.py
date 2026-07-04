import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
import datetime as dt
import seaborn as sns
sns.set_style("whitegrid")

start = dt.datetime(2024, 1, 1)
end = dt.datetime(2025, 5, 1)


def RSI(start, end, ticker):
    df = yf.download(ticker, start, end)
    df.columns = df.columns.droplevel(1)
    df['HIGH']=df['High'].rolling(14).max()
    df['LOW']=df['Low'].rolling(14).min()
    df['%K']=100*(df['Close']-df['LOW'])/(df['HIGH']-df['LOW'])
    df['%D']=df['%K'].rolling(3).mean()


    plt.subplot(311)
    plt.plot(df['Close'], 'r-', label='CLOSE_PRICE')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Close')
    plt.title('CLOSE')

    plt.subplot(312)
    plt.plot(df['%K'], 'b-', label='%K')
    plt.axhline(y=20, color='red', linestyle='--',
                linewidth=1.5)
    plt.axhline(y=80, color='red', linestyle='--',
                linewidth=1.5)
    plt.legend(loc="upper left")
    plt.ylabel('%K')
    plt.ylim(0, 100)
    plt.title('Stochastic')

    
    plt.subplot(313)
    plt.axhline(y=20, color='red', linestyle='--',
                linewidth=1.5)
    plt.axhline(y=80, color='red', linestyle='--',
                linewidth=1.5)
    plt.plot(df['%D'],'g-',label='%D')
    plt.legend(loc="upper left")
    plt.ylabel('%D')
    plt.ylim(0, 100)
    plt.title('Stochastic')
    plt.tight_layout(pad=2.0)
    plt.show()


RSI(start, end, "RELIANCE.NS")
