import numpy as np
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import os
import datetime as dt
from util import get_data
import indicators as inds
import marketsimcode as ms

class ManualStrategy(object):
    """
    A manual learner that can learn a trading policy using the same indicators used in StrategyLearner.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output.
    :type verbose: bool
    :param impact: The market impact of each transaction, defaults to 0.0
    :type impact: float
    :param commission: The commission amount charged, defaults to 0.0
    :type commission: float
    """

    # constructor
    def __init__(self, verbose=False, impact=0.005, commission=9.95):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.window = 20


    def author(self):
        return "azhou90"

    # function for trade manual strategy
    def testPolicy(self, symbol='IBM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):

        # get normalized price for indicator
        # print(symbol)
        price_norm = inds.get_price(symbol, sd, ed)

        # get amended indicators for strategy
        # indicator1 momentum
        momentum_value = inds.momentum(price_norm, window=self.window, plot=False)
        # indicator2 simple moving average(sma) - price
        sma_larger = inds.sma(price_norm, window=self.window, plot=False)
        # indicator3 bollinger bands percentage(bbp)
        bbp = inds.BBP(price_norm, window=self.window, plot=False)
        # indicator4 MACD - signal
        macd_larger = inds.MACD(price_norm)

        ############################ manual strategy  #####################################

        # initial trade dataframe
        trade_df = pd.DataFrame(index=price_norm.index)
        trade_df[symbol] = 0
        # date = pd.date_range(sd,ed)
        # trade_df = pd.DataFrame(date, columns=['Date'])
        # trade_df[symbol] =symbol


        # initial position long 1/ short -1/ out 0
        position = 0
        # manual strategy according to indicators
        for i in range(len(trade_df)):
            if (momentum_value[i] < - 0.1).item() or (sma_larger[i] < 0.4).item() or (bbp[i] < -0.6).item() or ( macd_larger[i] > 0.005).item():
                # print('yes')
                if position == 0:
                    # print('yes')
                    position = 1
                    # trade_df['Order'].iloc[i] = 'BUY'
                    # trade_df['Share'].iloc[i] = 1000
                    trade_df.iloc[i] = 1000
                elif position == -1:
                    # print('yes')
                    position = 1
                    # trade_df['Order'].iloc[i] = 'BUY'
                    # trade_df['Share'].iloc[i] = 2000
                    trade_df.iloc[i] = 2000
                else:
                    # print('yes')
                    position = 1
            elif (momentum_value[i] > 0.1).item() or (sma_larger[i] > 1.2).item() or (bbp[i] > 0.6).item() or (macd_larger[i] < -0.005).item():
            #     print('no')
                if position == 0:
                    position = -1
                    # trade_df['Order'].iloc[i] = 'SELL'
                    # trade_df['Share'].iloc[i] = 1000
                    trade_df.iloc[i] = -1000
                elif position == 1:
                    position = -1
                    # trade_df['Order'].iloc[i] = 'SELL'
                    # trade_df['Share'].iloc[i] = 2000
                    trade_df.iloc[i] = -2000
                else:
                    position = -1

        # trade_df = trade_df.loc[trade_df['Order'] != 'TBD'].reset_index()

        return trade_df

    def benchMark(self, symbol='IBM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        # date range
        dates = pd.date_range(sd, ed)

        prices_all = get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol]]  # only portfolio symbols
        trades_SPY = prices_all["SPY"]  # only SPY, for comparison later

        trades.values[:, :] = 0  # set them all to nothing
        trades.values[0, :] = 1000  # add a BUY at the start
        trades.values[-1, :] = -1000  # exit on the last day

        return trades

    def port_stats(self, portfolio):
        cumu_ret = (portfolio.iloc[-1] / portfolio.iloc[0] - 1).item()

        daily = portfolio.copy()
        daily.iloc[1:] = portfolio.iloc[1:] / portfolio.iloc[:-1].values - 1
        daily = daily.iloc[1:]

        std_ret = daily.std().item()
        mean_ret = daily.mean().item()
        sharpe_ratio = np.sqrt(252) * mean_ret / std_ret

        return cumu_ret, std_ret, mean_ret, sharpe_ratio

    def compareManual(self, symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000, sample="In-Sample"):

        # mnsg = ManualStrategy()
        # test_trade = mnsg.testPolicy(symbol='JPM')
        # result2 = ms.compute_portvals(test_trade)

        trade_df = self.testPolicy(symbol, sd, ed, sv)
        benchmark_df = self.benchMark(symbol, sd, ed, sv)

        trade_port = ms.compute_portvals(trade_df, start_val=sv, commission=self.commission, impact=self.impact)
        benchmark_port = ms.compute_portvals(benchmark_df, start_val=sv, commission=self.commission, impact=self.impact)


        cumu_ret_m, std_ret_m, mean_ret_m, sharpe_ratio_m = self.port_stats(trade_port)
        print(f"stats results for manual strategy: symbol {symbol} from {sd} to {ed} \n")
        print(f"cumulated return of {symbol} manual strategy is {cumu_ret_m}")
        print(f"daily return standard deviation of {symbol} manual strategy is {std_ret_m}")
        print(f"daily return mean of {symbol} manual strategy is {mean_ret_m}")
        print(f"sharpe ratio of {symbol} manual strategy is {sharpe_ratio_m}\n\n")

        cumu_ret_b, std_ret_b, mean_ret_b, sharpe_ratio_b = self.port_stats(benchmark_port)
        print(f"stats results for benchmark: symbol {symbol} from {sd} to {ed} \n")
        print(f"cumulated return of {symbol} benchmark is {cumu_ret_b}")
        print(f"daily return standard deviation of {symbol} benchmark is {std_ret_b}")
        print(f"daily return mean of {symbol} benchmark is {mean_ret_b}")
        print(f"sharpe ratio of {symbol} benchmark is {sharpe_ratio_b}\n\n")





        plt.figure(figsize=(10, 5))
        trade_port = trade_port/trade_port.iloc[0]
        benchmark_port = benchmark_port/benchmark_port.iloc[0]
        plt.plot(trade_port, label=f'{sample} manual strategy', c='r')
        plt.plot(benchmark_port, label=f'{sample} benchmark', c='g')
        long_idx = trade_df[trade_df.values>0].index
        short_idx = trade_df[trade_df.values < 0].index
        ymin = min(min(benchmark_port.values), min(trade_port.values))
        ymax = max(max(benchmark_port.values), max(trade_port.values))
        plt.vlines(long_idx, ymin= ymin, ymax=ymax, colors='b',
                   lw=.5, linestyles='--', label='Long')
        plt.vlines(short_idx, ymin= ymin, ymax=ymax, colors='k',
                   lw=.5, linestyles='--', label='Short')
        plt.xlabel('Date')
        plt.ylabel('Normalized portfolio value')
        plt.title(f'{sample} manual strategy vs. benchmark for JPM')
        plt.legend()
        plt.savefig(f'{sample}.png')



if __name__ == "__main__":
    msms = ManualStrategy()
    msms.compareManual(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000, sample="In-Sample")
    msms.compareManual(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000, sample="Out-Sample")



