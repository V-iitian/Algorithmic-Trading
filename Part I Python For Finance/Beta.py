import pandas as pd 
import matplotlib.pyplot
import datetime as dt
import yfinance as yf 

start = dt.datetime(2023,1,1)
end = dt.datetime(2026,7,10)
# data download 
tickers = ['^BSESN','RELIANCE.NS','INFY',"EICHERMOT.NS",
            "TITAN.NS",
            "HEROMOTOCO.NS",
            "ONGC.NS",
            "BRITANNIA.NS",
            "ADANIENT.NS",
            "MARUTI.NS",
            "RELIANCE.NS",
            "COALINDIA.NS",
            "ADANIPORTS.NS",
            "LTIM.NS",
            "HCLTECH.NS",
            "NESTLEIND.NS",
            "DRREDDY.NS",
            "TATACONSUM.NS",
            "ICICIBANK.NS",
            "GRASIM.NS",
            "BAJAJFINSV.NS",
            "HDFCLIFE.NS",
            "HINDALCO.NS",]
merged_df = yf.download('^NSEI',start,end)
# 1. First run your line to clear the level you don't want
merged_df.columns = merged_df.columns.droplevel(1)

# 2. Force the remaining names into clean strings
merged_df.columns = [str(col[0]) if isinstance(col, tuple) else str(col) for col in merged_df.columns]
merged_df = merged_df.rename(columns={"Close": '^NSEI'})
merged_df = merged_df.dropna()
merged_df = merged_df.drop(columns=['Volume','Open','High','Low'])
for ticker in tickers:
    df = yf.download(ticker,start,end)
    if df.empty:
        print(f'Data Not found for {ticker}')
        continue
    df.columns = df.columns.droplevel(1)
    df.columns = [str(col[0]) if isinstance(col, tuple) else str(col) for col in df.columns]
    df = df.dropna()
    df = df.drop(columns= ['Volume','Open','High','Low'])
    df = df.rename(columns={"Close": f'{ticker}'})
    merged_df = merged_df.merge(df,on='Date')


full_matrix = merged_df.corr()
result = full_matrix[['^NSEI', '^BSESN']]
print(result)






