import datetime as dt
import random
import numpy as np
import pandas as pd
import util as ut
import indicators as inds
import matplotlib.pyplot as plt
import indicators as indi
import marketsimcode as ms
import ManualStrategy
import StrategyLearner


def author():
    return "azhou90"

def exp2_result(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    msms = ManualStrategy.ManualStrategy()

    sl1 = StrategyLearner.StrategyLearner(impact=0, commission=0)
    sl1.add_evidence(symbol, sd, ed, sv)
    strategy_df_1 = sl1.testPolicy(symbol, sd, ed, sv)

    sl2 = StrategyLearner.StrategyLearner(impact=0.005, commission=0)
    sl2.add_evidence(symbol, sd, ed, sv)
    strategy_df_2 = sl2.testPolicy(symbol, sd, ed, sv)

    sl3 = StrategyLearner.StrategyLearner(impact=0.05, commission=0)
    sl3.add_evidence(symbol, sd, ed, sv)
    strategy_df_3 = sl3.testPolicy(symbol, sd, ed, sv)


    sl4 = StrategyLearner.StrategyLearner(impact=0.1, commission=0)
    sl4.add_evidence(symbol, sd, ed, sv)
    strategy_df_4 = sl4.testPolicy(symbol, sd, ed, sv)

    print('trade frequency metrics impact 0')
    frequency_1 = (strategy_df_1 != 0).sum().item()
    print(frequency_1)
    print('trade frequency metrics impact 0.002')
    frequency_2 = (strategy_df_2 != 0).sum().item()
    print(frequency_2)
    print('trade frequency metrics impact 0.005')
    frequency_3 = (strategy_df_3 != 0).sum().item()
    print(frequency_3)
    print('trade frequency metrics impact 0.007')
    frequency_4 = (strategy_df_4 != 0).sum().item()
    print(frequency_4)
    print('\n\n\n')




    # strategy_port_1 = ms.compute_portvals(strategy_df_1, start_val=sv, commission=commission, impact=0)
    # strategy_port_2 = ms.compute_portvals(strategy_df_2, start_val=sv, commission=commission, impact=0.005)
    # strategy_port_3 = ms.compute_portvals(strategy_df_3, start_val=sv, commission=commission, impact=0.05)
    # strategy_port_4 = ms.compute_portvals(strategy_df_4, start_val=sv, commission=commission, impact=0.1)

    strategy_port_1 = ms.compute_portvals(strategy_df_1,  commission=0, impact=0)
    strategy_port_2 = ms.compute_portvals(strategy_df_2,  commission=0, impact=0.002)
    strategy_port_3 = ms.compute_portvals(strategy_df_3,  commission=0, impact=0.005)
    strategy_port_4 = ms.compute_portvals(strategy_df_4, commission=0, impact=0.007)


    cumu_ret_1, std_ret_1, mean_ret_1, sharpe_ratio_1 = msms.port_stats(strategy_port_1)
    print(f"stats results for strategy learner: symbol {symbol} from {sd} to {ed} with impact = 0 \n")
    print(f"cumulated return with impact = 0 is {cumu_ret_1}")
    print(f"daily return standard deviation with impact = 0 is {std_ret_1}")
    print(f"daily return mean with impact = 0 is {mean_ret_1}")
    print(f"sharpe ratio with impact = 0 is {sharpe_ratio_1}\n\n")

    cumu_ret_2, std_ret_2, mean_ret_2, sharpe_ratio_2 = msms.port_stats(strategy_port_2)
    print(f"stats results for strategy learner: symbol {symbol} from {sd} to {ed} with impact = 0.002 \n")
    print(f"cumulated return with impact = 0.002  is {cumu_ret_2}")
    print(f"daily return standard deviation with impact = 0.002  is {std_ret_2}")
    print(f"daily return mean with impact = 0.002  is {mean_ret_2}")
    print(f"sharpe ratio with impact = 0.002  is {sharpe_ratio_2}\n\n")

    cumu_ret_3, std_ret_3, mean_ret_3, sharpe_ratio_3 = msms.port_stats(strategy_port_3)
    print(f"stats results for strategy learner: symbol {symbol} from {sd} to {ed} with impact = 0.005 \n")
    print(f"cumulated return with impact = 0.005 is {cumu_ret_3}")
    print(f"daily return standard deviation with impact = 0.005 is {std_ret_3}")
    print(f"daily return mean with impact = 0.005 is {mean_ret_3}")
    print(f"sharpe ratio with impact = 0.005 is {sharpe_ratio_3}\n\n")

    cumu_ret_4, std_ret_4, mean_ret_4, sharpe_ratio_4 = msms.port_stats(strategy_port_4)
    print(f"stats results for strategy learner: symbol {symbol} from {sd} to {ed} with impact = 0.007 \n")
    print(f"cumulated return with impact = 0.007 is {cumu_ret_4}")
    print(f"daily return standard deviation with impact = 0.007 is {std_ret_4}")
    print(f"daily return mean with impact = 0.007 is {mean_ret_4}")
    print(f"sharpe ratio with impact = 0.007 is {sharpe_ratio_4}\n\n")

    strategy_port_1 = strategy_port_1/strategy_port_1.iloc[0]
    strategy_port_2 = strategy_port_2/strategy_port_2.iloc[0]
    strategy_port_3 = strategy_port_3/strategy_port_3.iloc[0]
    strategy_port_4 = strategy_port_4/strategy_port_4.iloc[0]

    plt.figure(figsize=(10, 5))

    plt.plot(strategy_port_1, label='impact=0', c='b')
    plt.plot(strategy_port_2, label='impact=0.002', c='g')
    plt.plot(strategy_port_3, label='impact=0.005', c='y')
    plt.plot(strategy_port_4, label='impact=0.007', c='r')
    plt.xlabel('Date')
    plt.ylabel('Normalized portfolio value')
    plt.title('Experiment 2: Strategy Learner with different impact for JPM (commission=0)')
    plt.legend()
    plt.savefig('exp2.png')

if __name__ == "__main__":
    np.random.seed(1234567)

    exp2_result()