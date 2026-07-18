import datetime as dt 
import yfinance as yf 

start = dt.datetime(2025,1,1)
end = dt.datetime(2026,7,7)
data = yf.download('RELIANCE.NS',start,end)

data.columns = data.columns.droplevel(1)

data.to_csv('RELIANCE.csv',index='Date')