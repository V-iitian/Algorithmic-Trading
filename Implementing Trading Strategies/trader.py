import backtrader as bt

import datetime as dt

cerebro = bt.Cerebro()

cerebro.broker.set_cash(1000000)

print("starting portfolio value:%0.2f" % cerebro.broker.getvalue())
data = bt.feeds.YahooFinanceCSVData(
    dataname='Oracle_Clean.csv',
    fromdate=dt.datetime(2000, 1, 1),
    todate=dt.datetime(2000, 12, 31),
    reverse=False
)
cerebro.adddata(data)
cerebro.run()

print("Final portfolio Value : %0.2f" % cerebro.broker.getvalue())
