""""""
import numpy as np


"""  		  	   		   	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import random  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
import util as ut
import indicators as inds

import RTLearner as rl
import BagLearner as bl
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
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
        self.learner = bl.BagLearner(learner=rl.RTLearner, kwargs={"leaf_size":5}, bags=25)
        self.window = 20

        self.YBUY = 0.012
        self.YSELL = -0.012
        self.NDAY = 7

    def author(self):
        return "azhou90"
  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		  	   		   	 		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),
        sv=100000,
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        # add your code to do learning here

        ########## create X_train ##############

        # get nomarlized price for indicator
        # print(symbol)
        # price_norm = inds.get_price(symbol, sd, ed)

        # dates = pd.date_range(sd, ed)

        # price_all = ut.get_data([symbol], dates)
        # price_norm =price_all[[symbol]]
        price_norm = inds.get_price(symbol,sd,ed)

        # get amended indicators for strategy
        # indicator1 momentum
        momentum_value = inds.momentum(price_norm, window=self.window, plot=False)
        # indicator2 simple moving average(sma) - price
        sma_larger = inds.sma(price_norm, window=self.window, plot=False)
        # indicator3 bollinger bands percentage(bbp)
        bbp = inds.BBP(price_norm, window=self.window, plot=False)
        # indicator4 macd - signal
        macd_larger = inds.MACD(price_norm)

        # create X_train for learner
        # df = pd.concat((momentum_value,sma_larger,bbp,macd_larger), axis=1)
        df = pd.DataFrame(np.hstack([momentum_value, sma_larger, bbp, macd_larger]))
        df.fillna(0, inplace=True)
        df.columns=['momentum_value','sma_larger','bbp','macd_larger']


        X_train = df


        ######### create Y_train ########
        #initial NDAY, YBUY, YSELL
        NDAY= self.NDAY
        YBUY = self.YBUY
        YSELL = self.YSELL

        # n_days return
        # nday_return = np.zeros(len(price_norm) - NDAY)
        nday_return = pd.DataFrame(index=price_norm.index[:-NDAY])
        nday_return['return'] = 0

        # print(nday_return)

        for i in range(len(nday_return)):
            nday_return.iloc[i] = price_norm.iloc[i + NDAY].item() / price_norm.iloc[i].item() - 1

        # print(price_norm.iloc[10])
        # print(nday_return)
        # determine the position
        # initial trade dataframe
        Y_train = pd.DataFrame(index=price_norm.index)
        Y_train['Position'] = 0

        # determine buy or sell according to nday_return
        for i in range(len(nday_return)):
            if nday_return.iloc[i].item() > (YBUY + self.impact):
                Y_train.iloc[i] = 1
            elif nday_return.iloc[i].item() < (YSELL - self.impact):
                Y_train.iloc[i] = -1
        X_train = X_train[:-NDAY]
        Y_train = Y_train[:-NDAY]
        # train the learner
        # print(Y_train)

        self.learner.add_evidence(X_train, Y_train)


        # Y_pred = self.learner.query(X_train)
        # print(Y_pred)
        # print(Y_train.to_numpy().squeeze())
        # print(np.sum(Y_train.to_numpy().squeeze() == Y_pred)/len(Y_pred))

        # print(nday_return)
        # print(X_train)
        # print(Y_train)
  		  	   		   	 		  		  		    	 		 		   		 		  
        # example usage of the old backward compatible util function  		  	   		   	 		  		  		    	 		 		   		 		  
        # syms = [symbol]
        # dates = pd.date_range(sd, ed)
        # prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        # prices = prices_all[syms]  # only portfolio symbols
        # prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
        # if self.verbose:
        #     print(prices)
  		  	   		   	 		  		  		    	 		 		   		 		  
        # example use with new colname  		  	   		   	 		  		  		    	 		 		   		 		  
        # volume_all = ut.get_data(
        #     syms, dates, colname="Volume"
        # )  # automatically adds SPY
        # volume = volume_all[syms]  # only portfolio symbols
        # volume_SPY = volume_all["SPY"]  # only SPY, for comparison later
        # if self.verbose:
        #     print(volume)
  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		   	 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=100000,
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		   	 		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		   	 		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		   	 		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  

        ########## create X_test ##############

        # get nomarlized price for indicator
        # print(symbol)
        price_norm = inds.get_price(symbol, sd, ed)
        # dates = pd.date_range(sd, ed)
        #
        # price_all = ut.get_data([symbol], dates)
        # price_norm =price_all[[symbol]]

        # get amended indicators for strategy
        # indicator1 momentum
        momentum_value = inds.momentum(price_norm, window=self.window, plot=False)
        # indicator2 simple moving average(sma) - price
        sma_larger = inds.sma(price_norm, window=self.window, plot=False)
        # indicator3 bollinger bands percentage(bbp)
        bbp = inds.BBP(price_norm, window=self.window, plot=False)
        # indicator4 macd - signal
        macd_larger = inds.MACD(price_norm)

        # create X_test for learner
        # df = pd.concat((momentum_value,sma_larger,bbp,macd_larger),axis=1)
        df = pd.DataFrame(np.hstack([momentum_value, sma_larger, bbp, macd_larger]))
        df.fillna(0, inplace=True)
        df.columns = ['momentum_value', 'sma_larger', 'bbp', 'macd_larger']

        X_test = df
        # X_test = X_test[:-self.NDAY]

        ######### predict Y_pred and trade_df ########
        Y_pred = self.learner.query(X_test)
        # print(Y_pred)

        #initial trade_df
        trade_df = pd.DataFrame(index=price_norm.index)
        trade_df[symbol] = 0

        #initial position
        position = 0
        for i in range(len(Y_pred)):
            if position == 0:
                # position = Y_pred[i]
                if Y_pred[i] == 1:
                    trade_df.iloc[i] = 1000
                    position = 1
                elif Y_pred[i] == -1:
                    trade_df.iloc[i] = -1000
                    position = -1
            elif position == - 1 :
                # position = Y_pred[i]
                if Y_pred[i] == 1:
                    trade_df.iloc[i] = 2000
                    position = 1
                elif Y_pred[i] == 0:
                    trade_df.iloc[i] = 1000
                    position = 0
            elif position == 1:
                # position = Y_pred[i]
                if Y_pred[i] == 0:
                    trade_df.iloc[i]= -1000
                    position = 0
                elif Y_pred[i] == -1:
                    trade_df.iloc[i] = -2000
                    position = -1



        # print(trade_df)
        return trade_df
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")
    # sl = StrategyLearner()
    # sl.add_evidence(symbol='ML4T-220', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2008, 12, 31), sv=100000)
    # print(sl)
    # trade_df = sl.testPolicy(symbol='ML4T-220', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2008, 12, 31), sv=100000)
    # print(trade_df)