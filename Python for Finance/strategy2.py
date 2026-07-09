import backtrader as bt 
class MAcrossover(bt.Strategy):
    params = (
        ('fast',5),
        ('slow',88),
    )

    def log(self,txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    
    def __init__ (self):
        self.dataclose = self.datas[0].close

        # order variables will contain ongoing order details/status
        self.order = None 
        self.bar_executed = 0
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0],period=self.params.slow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0],
                                                          period=self.params.fast)
        
    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            # An Active Buy/Sell order has been submitted/accepted-Nothing to do 
            return 
        
        # check if an order has been completed 
        # Attention: Broker could reject order if not enough cash 
        if order.status in [order.completed]:
            if order.isbuy():
                self.log(f'Buy Exceuted, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'Sell Exceuted, {order.executed.price:.2f}')
            self.bar_executed = len(self)
            #len(self) returns an integer representing the current bar number ( or the current row index)
        elif order.status in [order.Canceled, order.Margin , order.Rejected]:
            self.log('Order Cancelled/Margin/Rejected')
        self.order = None
    
    def next(self):
        # check for open orders 
        # its like if i have already sent an order of buying or selling to my broker 
        if self.order:
            return
        # check if we are in market
        if not self.position:
            # we are not in the market, look for a signal to Open trades 

            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                self.log(f'BUY Created {self.dataclose[0]:.2f}')
                # keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            
            # otherwise if the 20 SMA is below the 50 SMA 
            elif self.fast_sma[0]<self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1] :
                self.log(f'SELL Created {self.dataclose[0]:.2f}')
                # keep track of the crated order to avoid 2nd order
                self.order = self.sell() # used for shorting 
                # When you call self.sell(), you are instructing the broker to sell a specific number of shares, completely regardless of what is currently in your portfolio
        
        else:
            # We are already in the market, look for a signal to Close Trades
            # We will simply exit five bars after entering the trade. 
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE Created {self.dataclose[0]:.2f}')
                # keep track of the crated order to avoid 2nd order
                self.order = self.close()
                # When you call self.close(), Backtrader looks at your current open position and automatically calculates the exact order needed to bring your position to exactly 0. You do not need to specify a size.


