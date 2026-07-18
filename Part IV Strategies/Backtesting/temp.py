import datetime as dt
import backtrader as bt 

# initiate Cerebro Engine 
cerebro = bt.Cerebro(stdstats = False)

# set data parameters and add to Cerebro
data1 = bt.feeds.GenericCSVData(
        dataname = 'TSLA.csv',
        dtformat='%Y-%m-%d',
        # setting fot testing data 
        fromdate = dt.datetime(2024,1,1),
        todate = dt.datetime(2026,1,1),
        datetime=0,
        open=4,
        high=2,
        low=3,
        close=1,
        volume=5,
        openinterest = -1,
        headers = True
    )
cerebro.adddata(data1)

data2 = bt.feeds.GenericCSVData(
        dataname = 'AAPL.csv',
        dtformat='%Y-%m-%d',
        # setting fot testing data 
        fromdate = dt.datetime(2024,1,1),
        todate = dt.datetime(2026,1,1),
        datetime=0,
        open=4,
        high=2,
        low=3,
        close=1,
        volume=5,
        openinterest = -1,
        headers = True
    )


data2.compensate(data1) # let the system know ops on data1 affect data2
data2.plotinfo.plotmaster = data1
data2.plotinfo.sameaxis = True

cerebro.adddata(data2)

cerebro.run()
cerebro.plot(style='candlesticks')