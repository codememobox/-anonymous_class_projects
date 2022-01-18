import datetime as dt
import os

import numpy as np

import pandas as pd
from util import get_data, plot_data


def author():
    return "azhou90"


def compute_portvals(
        trade_df ,
        start_val=100000,
        commission= 9.95,
        impact= 0.005
):
    sd = trade_df.index[0]
    ed = trade_df.index[-1]
    symbol = trade_df.columns.item()
    dates = pd.date_range(sd, ed)

    cash = start_val
    share = 0

    prices_all = get_data([symbol], dates)
    trades = prices_all[[symbol]]

    out_df = pd.DataFrame(index=trade_df.index)
    out_df[symbol] = 0

    port = 0

    for i in range(len(trade_df)):
        if trade_df.iloc[i].item() > 0:
            cash = cash - trade_df.iloc[i].item() * (trades.iloc[i].item() * (1 + impact)) - commission
            share = share + trade_df.iloc[i].item()
            port = share * trades.iloc[i].item()
            out_df.iloc[i] = cash+port
        elif trade_df.iloc[i].item() < 0:
            cash = cash - trade_df.iloc[i].item() * (trades.iloc[i].item() * (1 - impact)) - commission
            share = share + trade_df.iloc[i].item()
            port = share * trades.iloc[i].item()
            out_df.iloc[i] = cash+port
        else:
            port = share * trades.iloc[i].item()
            out_df.iloc[i] = cash+port

    # df_out = pd.DataFrame(data=total_value, index=trade_df.index, columns=[symbol])

    return out_df
