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

def exp1_result(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000, commission=9.95, impact=0.005):
    msms = ManualStrategy.ManualStrategy()
    slsl = StrategyLearner.StrategyLearner()
    slsl.add_evidence(symbol, sd, ed, sv)

    manual_df = msms.testPolicy(symbol, sd, ed, sv)
    benchmark_df = msms.benchMark(symbol, sd, ed, sv)
    strategy_df = slsl.testPolicy(symbol, sd, ed, sv)

    manual_port = ms.compute_portvals(manual_df, start_val=sv, commission=commission, impact=impact)
    # manual_port = ms.compute_portvals(manual_df)
    benchmark_port = ms.compute_portvals(benchmark_df, start_val=sv, commission=commission, impact=impact)
    # benchmark_port = ms.compute_portvals(benchmark_df)
    strategy_port = ms.compute_portvals(strategy_df,start_val=sv, commission=commission, impact=impact)
    # strategy_port = ms.compute_portvals(strategy_df)

    cumu_ret_m, std_ret_m, mean_ret_m, sharpe_ratio_m = msms.port_stats(manual_port)
    print(f"stats results for manual strategy: symbol {symbol} from {sd} to {ed} \n")
    print(f"cumulated return of {symbol} manual strategy is {cumu_ret_m}")
    print(f"daily return standard deviation of {symbol} manual strategy is {std_ret_m}")
    print(f"daily return mean of {symbol} manual strategy is {mean_ret_m}")
    print(f"sharpe ratio of {symbol} manual strategy is {sharpe_ratio_m} \n\n")

    cumu_ret_b, std_ret_b, mean_ret_b, sharpe_ratio_b = msms.port_stats(benchmark_port)
    print(f"stats results for benchmark: symbol {symbol} from {sd} to {ed} \n")
    print(f"cumulated return of {symbol} benchmark is {cumu_ret_b}")
    print(f"daily return standard deviation of {symbol} benchmark is {std_ret_b}")
    print(f"daily return mean of {symbol} benchmark is {mean_ret_b}")
    print(f"sharpe ratio of {symbol} benchmark is {sharpe_ratio_b}\n\n")

    cumu_ret_s, std_ret_s, mean_ret_s, sharpe_ratio_s = msms.port_stats(strategy_port)
    print(f"stats results for strategy learner: symbol {symbol} from {sd} to {ed} \n")
    print(f"cumulated return of {symbol} strategy learner is {cumu_ret_s}")
    print(f"daily return standard deviation of {symbol} strategy learner is {std_ret_s}")
    print(f"daily return mean of {symbol} strategy learner is {mean_ret_s}")
    print(f"sharpe ratio of {symbol} strategy learner is {sharpe_ratio_s}\n\n")

    plt.figure(figsize=(10, 5))

    manual_port = manual_port/manual_port.iloc[0]
    benchmark_port = benchmark_port/benchmark_port.iloc[0]
    strategy_port = strategy_port/strategy_port.iloc[0]

    plt.plot(manual_port, label='Manual strategy', c='r')
    plt.plot(benchmark_port, label='Benchmark', c='g')
    plt.plot(strategy_port, label='Strategy lerner', c='b')
    plt.xlabel('Date')
    plt.ylabel('Normalized portfolio value')
    plt.title('Experiment 1: In-sample Manual Strategy vs. Strategy Learner vs. Benchmark for JPM')
    plt.legend()
    plt.savefig('exp1.png')

if __name__ == "__main__":
    np.random.seed(1234567)

    exp1_result()