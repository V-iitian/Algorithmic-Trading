import backtrader as bt
import datetime 
from strategy2 import * 


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    data = bt.feeds.GenericCSVData(
        dataname = 'TSLA.csv',
        dtformat='%Y-%m-%d',
        # setting fot testing data 
        fromdate = datetime.datetime(2024,1,1),
        todate = datetime.datetime(2026,1,1),
        datetime=0,
        open=4,
        high=2,
        low=3,
        close=1,
        volume=5,
        openinterest = -1,
        headers = True
    )

    # settings for out-of-sample data 
    # fromdate = datetim.datetime(2025,7,1)
    # todate = datetime.datetime(2026,1,1)
    cerebro.adddata(data)
    # adding Strategy to cerebro
    cerebro.addstrategy(MAcrossover)
    # optimization
    # cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
    # cerebro.optstrategy(MAcrossover)


    # default position size 
    cerebro.addsizer(bt.sizers.SizerFix,stake=3)
    #run cerebro engine 
    start_portfolio_value = cerebro.broker.getvalue()
    cerebro.run()
    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value-start_portfolio_value
    print(f'starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value {end_portfolio_value:2f}')
    print(f'PnL : {pnl:.2f}')
    cerebro.plot()
    # optimized_runs = cerebro.run(maxcpus = 1)

    # final_result_list =[]
    # for run in optimized_runs:
    #     for strategy in run:
    #         PnL = round(strategy.broker.get_value()-10000,2)
    #         sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
    #         final_result_list.append([strategy.params.fast,strategy.params.slow,sharpe['sharperatio'],PnL])

    # sort_by_sharpe = sorted(final_result_list,key=lambda x: x[2],reverse = True)

    # for line in sort_by_sharpe[:5]:
    #     print(line)


"""
We have included from strategy import * which will make it easier to call new strategies from the main script as we create them. Also included towards the end of the script are some details regarding portfolio values and our default position size, which has been set to 3 shares.

The command cerebro.broker.getvalue() allows you to obtain the value of the portfolio at any time. We grab the starting value by calling it before running cerebro and then call it once again after to get the ending portfolio value. We can see our profit or loss by subtracting the end value from the starting value
"""


"""
after running optimisation strategy i got 5 and 88 mas performed best now we will apply this to our out of sample data """