# indicators.py
# Code implementing your indicators as functions that operate on DataFrames.
# The “main” method in indicators.py should generate the charts that illustrate your indicators in the report.

import numpy as np
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import os
import datetime as dt

from util import get_data

def author():
    return "azhou90"

def get_price(sym, start_date, end_date):
    '''
    Helper function: get prices given symbol
    :param sym:
    :param start_date:
    :param end_date:
    :return:
    '''
    # if not isinstance(sym, list):
    #     sym = [sym]
    dates = pd.date_range(start=start_date, end=end_date)
    # prices = get_data(sym, dates, addSPY=False)
    # prices.ffill(inplace=True)
    # prices.bfill(inplace=True)
    #AMEND FOR PROJECT 8
    prices_all = get_data([sym], dates)   # automatically adds SPY
    prices = prices_all[[sym]]

    # Normalize price
    prices = prices/prices.iloc[0]
    return prices

def sma(prices, window=10, plot=False):
    '''
    Indicator 1: Simple Moving Average
    :param prices:
    :param window:
    :return:
    '''
    sma_value = prices.rolling(window).mean()
    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(prices, label='Normalized price')
        plt.plot(sma_value, label='Simple Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.title(f'Simple Moving Average, window={window}')
        plt.legend()
        plt.savefig('./fig/sma.png')
        # plt.show()
    #return for project6
    # return sma_value
    # amend code for project 8
    result = (prices/sma_value).to_numpy()
    return result
def BBP(prices, window=10, plot=False):
    '''
    Indicator 2: Bollinger Bands Percentage
    :param price:
    :param window:
    :return:
    '''
    mean = prices.rolling(window).mean()
    stdev = prices.rolling(window).std()
    upper = mean + 2 * stdev
    lower = mean - 2 * stdev
    # bb_value = (prices - lower) / (upper - lower)
    bb_value = (prices - mean) / (2 * stdev)
    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(prices, label='Normalized price')
        plt.plot(upper, label='Upper band')
        plt.plot(lower, label='Lower band')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.title(f'Bollinger Bands, window={window}')
        plt.legend()
        plt.savefig('./fig/BB.png')
        # plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(prices, label='Normalized price')
        plt.plot(bb_value, label='Bollinger Bands Percentage')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.title(f'Bollinger Bands Percentage, window={window}')
        plt.legend()
        plt.savefig('./fig/BBP.png')
        # plt.show()
    # project 6's return
    # return bb_value, upper, lower
    # amend for project 8
    return bb_value.to_numpy()

def momentum(prices, window=10, plot=False):
    '''
    Indicator 3: Momentum
    :param prices:
    :param window:
    :return:
    '''
    momentum_value = prices/prices.shift(window) - 1
    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(prices, label='Normalized price')
        plt.plot(momentum_value, label='Momentum')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.title(f'Momentum, window={window}')
        plt.legend()
        plt.savefig('./fig/momentum.png')
        # plt.show()
    return momentum_value.to_numpy()

def MACD(prices, short_window=12, long_window=26, plot=False):
    '''
    Indicator 4: Moving Average Convergence Divergence
    :param prices:
    :return:
    '''
    short = prices.ewm(span=short_window,adjust=False).mean()
    long  = prices.ewm(span=long_window,adjust=False).mean()
    macd_value = long - short
    signal = macd_value.ewm(span=9, adjust=False).mean()
    if plot:
        plt.figure(figsize=(10, 5))
        # plt.plot(prices, label='Normalized price')
        plt.plot(macd_value, label='MACD')
        plt.plot(signal, label='Signal')
        plt.xlabel('Date')
        plt.ylabel('Difference between long and short EMAs')
        plt.title('Moving Average Convergence Divergence')
        plt.legend()
        plt.savefig('./fig/macd.png')
        # plt.show()
    # project 6's return
    # return macd_value, signal
    # amend for project 8
    result = macd_value - signal
    return result.to_numpy()


if __name__ == "__main__":
    sym = 'JPM'
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009,12,31)

    prices = get_price(sym, start_date, end_date)

    # print(sma(prices))
    # a = sma(prices)
    # print(a)
    # b = BBP(prices)
    # df=pd.concat((a,b), axis=1)
    # df.fillna(0,inplace=True)
    # df.columns=['sma','bbp']
    # print(len(prices))
    # print(momentum(prices))
    # print(MACD(prices))
    # volatility(prices)
    # print(prices)

    trade = pd.DataFrame(index=prices.index[:-10])
    trade['position']=0
    print(trade)
    # print(sma(prices))
    # print(BBP(prices))
    # print(momentum(prices))
    # print(MACD(prices))
    # print(volatility(prices))

    # print(prices.iloc[8]/ prices.iloc[1])