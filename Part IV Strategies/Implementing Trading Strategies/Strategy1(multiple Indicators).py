import backtrader as bt
import pandas as pd 
import numpy as np  
import datetime as dt
import quantstats

#intialising backtrader 

import backtrader as bt

# commision policy of the broker and taxes included 
# for Zerodha intraday trading commission is max(Rs20,0.03% of the trade amount) but in our case we'll always cash nd carry 
# making commission Class 
class ZerodhaCommission(bt.CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_PERC),
        ('percabs', True),
        
        # --- Strategy Mode Toggle ---
        ('is_intraday', True),         # Set to False for Delivery (CNC) strategies
        
        # --- Common Charges ---
        ('exchange_txn', 0.0000322),   # NSE txn charge (~0.00322%)
        ('gst_rate', 0.18),            # 18% GST on (Brokerage + Txn Charge)
        ('sebi_turnover', 0.000001),   # ₹10 per crore

        # --- Delivery (CNC) Rates ---
        ('stt_delivery', 0.001),       # 0.1% (BUY and SELL)
        ('stamp_delivery', 0.00015)    # 0.015% (BUY only)
    )

    def _getcommission(self, size, price, pseudoexec):
        turnover = abs(size) * price
        
        brokerage = 0.0
        stt = 0.0
        stamp = 0.0
        # 2. DELIVERY LOGIC (CNC)
        brokerage = 0.0 # Zerodha charges 0 brokerage for delivery
        if size > 0:  # BUY
            stamp = turnover * self.p.stamp_delivery
        elif size < 0:  # SELL
            stt = turnover * self.p.stt_delivery # STT applies to sell in delivery
        # 3. COMMON CHARGES (Apply to both modes)
        txn_charge = turnover * self.p.exchange_txn
        gst = (brokerage + txn_charge) * self.p.gst_rate
        sebi = turnover * self.p.sebi_turnover
        return brokerage + txn_charge + gst + sebi + stt + stamp

class Strategy1(bt.Strategy):

    # all the parameters value that we are using, You can tweek values directly from here for optimising 
    params = (('short_ma',9),('long_ma',50),('signal',25),('ATR_period',10))
    
    def log(self,txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        # order is submitted or accepted by broker but not yet executed 

        if order.status in [order.Submitted,order.Accepted]:
            return
        # order is completed from the broker side 
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXCEUTED, {order.executed.price:.2f}')
            if order.issell():
                self.log(f'Sell Exceuted, {order.executed.price:.2f}')
        
        # your order has been rejected 
        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('Order Cancelled/Margin/Rejected')

        self.order = None
        return
    
    def __init__(self):
        # Candlestick Data 
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataopen = self.datas[0].open
        self.Volume = self.datas[0].volume
        ### All Indicators 
        ## macd indicator 
        self.macd = bt.indicators.MACD(self.dataclose,period_me1 = self.params.short_ma , period_me2 = self.params.long_ma, period_signal = self.params.signal ) 
        ## ATR indicator for Stop loss and volatiltiy check 
        self.atr = bt.indicators.AverageTrueRange(self.datas[0],period = self.params.ATR_period)
        ## rsi for momentum and works well in sideways market 
        self.rsi = bt.indicators.RSI(self.dataclose,period = self.params.ATR_period)
        ## for trend confirmation
        self.MA = bt.indicators.MovingAverageSimple(self.dataclose,period = self.params.short_ma)
        self.MA2 = bt.indicators.MovingAverageSimple(self.dataclose,period = self.params.long_ma)
        self.VolumeMA = bt.indicators.MovingAverageSimple(self.datas[0].volume,period = 14)
        #initialising trailing loss 
        ## initialising order variable 
        self.order = None

    def next(self):
        Volatilty_ = (self.atr[0]/self.dataclose[0])*100
        Bottom = self.MA[0]-self.atr[0]
        Up = self.MA[0]+self.atr[0]

        # if order is not executed , Accepted , Submitted yet ?
        if self.order:
            return
        
        #First let's create a strategy that will implement one Order at a time 
        if not self.position:
            # Buy Signal 
            if self.macd.macd[0]>0 and self.macd.macd[-1]<0 :
                if Volatilty_ > 5:
                    return
                if Volatilty_<1:
                    return
                if self.dataclose[0]<= Bottom*1.2:
                    if self.dataclose[0]>self.MA2:
                        self.order = self.buy()
                if self.dataclose[0]>=Up*0.8:
                    #Strong Uptrend Coming 
                    # check for Volume MA 
                    if self.Volume>= self.VolumeMA:
                        if self.dataclose[0]>=self.MA2:
                            self.order = self.buy(size=10)
                    else:
                        if self.dataclose[0]>=self.MA2:
                            self.order = self.buy(size=5)
            elif self.macd.macd[0]<0 and self.macd.macd[-1]>0:
                if self.dataclose[0]>=Up*0.9:
                    if self.dataclose[0]<=self.MA2:
                        self.order = self.sell()
                elif self.dataclose[0]<=1.2*Bottom:
                    #Strong Downtrend 
                    # check for Volume MA 
                    if self.Volume>= self.VolumeMA:
                        if self.dataclose[0]<=self.MA2:
                            self.order = self.sell(size=10)
                    else:
                        if self.dataclose[0]<= self.MA2:
                            self.order = self.sell(size=5)
        elif self.position:
            # i am long currently
            if Volatilty_>5:
                self.order = self.close()
            elif self.position.size>0:
                if self.macd.macd[0]<0 and self.macd.macd[-1]>0:
                    self.order = self.close()
                    self.log('Close Executed')
                # stoploss type thing
                if self.dataclose[0]<0.8*Bottom:
                    self.order = self.close()
                    self.log('Close Executed')
            
            elif self.position.size<0:
                if self.macd.macd[0]>0 and self.macd.macd[-1]<0:
                    self.order = self.close()
                    self.log('Close Executed')
                
                if self.dataclose[0]>1.2*Up:
                    self.order = self.close()
                    self.log('Close Executed')
                
            

if __name__ == '__main__':
        
        # data processing
        # we will be using 2020-2024 data for optimising or tweaking our strategy and then we will backtest it on 2025-26 data 
        data = bt.feeds.GenericCSVData(
            dataname = 'RELIANCE.csv',
            headers = True,
            separators =',',
            datetime = 0, close = 1,open=2,high=3,low=4,volume = 5,
            openinterest = -1,
            dtformat='%Y-%m-%d'
        )
        cerebro = bt.Cerebro()
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
        zerodha_comm = ZerodhaCommission()
        cerebro.broker.addcommissioninfo(zerodha_comm)
        # equity exchange charges 
        cerebro.adddata(data)
        cerebro.addstrategy(Strategy1)
        cerebro.addsizer(bt.sizers.FixedSize, stake=1)
        cerebro.broker.setcash(100000)
        results = cerebro.run()
        strat = results[0]
        print(cerebro.broker.getvalue())
        print(f'NET PnL {cerebro.broker.getvalue()-100000}')
        portfolio_stats = strat.analyzers.getbyname('PyFolio')
        returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
        returns.index = returns.index.tz_convert(None)   
        quantstats.reports.html(returns, output='strategy1.html', title='RELIANCE.NS(2020 to 2024)')
        cerebro.plot()




