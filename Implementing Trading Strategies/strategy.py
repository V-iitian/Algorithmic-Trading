import backtrader as bt
import datetime as dt
import pandas as pd
import yfinance as yf 


class IntradayCommissionStrategy(bt.Strategy):
    def notify_trade(self, trade):
        # We only want to evaluate trades that have been fully closed
        if not trade.isclosed:
            return
        # Convert Backtrader's float-based timestamps to standard Python dates
        open_date = bt.num2date(trade.dtopen).date()
        close_date = bt.num2date(trade.dtclose).date()
        # Check if the trade was held overnight (Delivery)
        if open_date != close_date:
            # Backtrader tracks the total commission charged for both legs of this trade
            refund_amount = trade.commission
            
            # Add the cash back to the broker balance
            self.broker.add_cash(refund_amount)
            
            print(f"Delivery trade: Held overnight. Refunded commission: {refund_amount:.2f}")
        else:
            # The trade was opened and closed on the same day
            print(f"Intraday trade: Same day execution. Commission paid:{trade.commission:.2f}")

class SMACrossover(bt.Strategy):
    # 1. Define the parameters for your moving averages
    params = (
        ('fast_length', 10),
        ('slow_length', 30)
        ,('rsi_period',14),
        ('Volume_period',14)
    )

    def log(self,txt,dt=None):

        dt = dt or self.datas[0].datetime.date(0)
        print('%s : %s'%(dt.isoformat(), txt))

    def __init__(self):
        # 2. Initialize the indicators
        # Backtrader automatically calculates these for every new data point
        sma_fast = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_length
        )
        sma_slow = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_length
        )
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

        # 3. Create the signal generator
        # CrossOver returns 1 (upward cross), -1 (downward cross), or 0 (no cross)
        self.crossover = bt.indicators.CrossOver(sma_fast, sma_slow)
        self.volume_avg = bt.indicators.SimpleMovingAverage(
            self.data.volume,
            period = self.params.Volume_period
        )
    def next(self):
        # 4. The core logic evaluated on every new bar/candle
        self.log('Close, %.2f' %self.data.close[0])
        # Check if we already have an open position in the market
            # We are not in the market, look for a buy signal
        if (self.crossover > 0 or (self.rsi[0] < 30 and self.rsi[-1]>30)) and (self.data.volume[0]>self.volume_avg):
            self.log('Buy Create,%.2f' %self.data.close[0])
            self.buy()  # Execute a buy order

        elif self.rsi[-1]>70 and self.rsi[0]>70 and self.volume_avg<self.data.volume[0]:
            self.log('Buy Create,%.2f' %self.data.close[0])
            self.buy()

        
        # We are in the market, look for a sell signal to exit
        if (self.crossover < 0 or (self.rsi[0]>70 and self.rsi[-1]<70)) and (self.data.volume[0]>self.volume_avg):
            self.log('Sell Create, %.2f' %self.data.close[0])
            self.close()  # Sell our current holdings
        if self.rsi[-2]<30 and self.rsi[-1]<30 and self.rsi[0]<30 and (self.data.volume[0]>self.volume_avg):
            self.log('Sell Create, %.2f' %self.data.close[0])
            self.close()  # Sell our current holdings

    
    def stop(self):
        print("\n--- INDIVIDUAL STOCK HOLDINGS ---")
        
        # Loop through all data feeds (stocks) passed to cerebro
        for data in self.datas:
            position = self.getposition(data)
            
            # If size is not 0, we hold this stock
            if position.size != 0:
                # Calculate current market value: Number of shares * Last closing price
                current_market_value = position.size * data.close[0]
                
                print(f"Stock: {data._name}")
                print(f"  Shares Held   : {position.size}")
                print(f"  Current Price : ₹ {data.close[0]:.2f}")
                print(f"  Total Value   : ₹ {current_market_value:.2f}")

if __name__ == '__main__':
    # Initialize the engine
    cerebro = bt.Cerebro()

    # Add the strategy to the engine
    cerebro.addstrategy(SMACrossover)

    # NOTE: You will need to load a data feed here for the engine to process
    # Example using a local CSV file:

    data = bt.feeds.GenericCSVData(dataname='Oracle_Clean.csv',
                                   dtformat='%Y-%m-%d',
                                   headers = True,
                                   reverse=False)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.adddata(data)

    # Set starting capital
    initial_cash = 1000
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.0003)
    # Run the backtest
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    print('final profit value:',cerebro.broker.getvalue()-initial_cash)
    cerebro.plot()
