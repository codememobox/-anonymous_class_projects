import ManualStrategy
import StrategyLearner
from experiment1 import exp1_result
from experiment2 import exp2_result

import datetime as dt
import random
import numpy as np


def author():
    return "azhou90"

if __name__ == "__main__":
    msms = ManualStrategy.ManualStrategy()
    msms.compareManual(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000, sample="In-Sample")
    msms.compareManual(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000, sample="Out-Sample")
    np.random.seed(1234567)
    exp1_result()
    np.random.seed(1234567)
    exp2_result()
