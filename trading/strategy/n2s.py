# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 北向资金分析
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

from trading.collector.constant import (stock_n2s_path)

"""
1.当日北向资金净买入 > 过去252个交易日的北向资金净买入均值 + 2倍标准差,则第二个交易日全仓买入沪深300
2.当日北向资金净买入 < 过去252个交易日的北向资金净买入均值 - 2倍标准差,则第二个交易日清仓卖出沪深300
3.北向开始时间2016-12-05日, 252个交易日大约一年,最早能开始回测的时间大概在2018-01-01
"""


def show_n2s_sign(code=None, start_date='2017-01-01', end_date=None):
    # 设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False

    df = pd.read_csv(os.path.join(stock_n2s_path, 'n2s.csv'), encoding='utf-8')
    df.index = pd.DatetimeIndex(df['日期'])
    df = df.sort_index()
    ma252 = df['当日成交净买额'].rolling(252).mean()
    std = df['当日成交净买额'].rolling(252).std()
    up_line = ma252 + 2*std
    down_line = ma252 - 2*std
    df['mean'] = ma252
    df['std'] = std
    df['up'] = up_line
    df['down'] = down_line
    if(end_date is None):
        end_date = datetime.datetime.today().strftime("%Y-%m-%d")
    df = df[start_date:end_date]
    plt.plot(df.index, df['up'], color="green", label="up_line")
    plt.plot(df.index, df['down'], color="black", label="down_line")
    plt.plot(df.index, df['当日成交净买额'], color="red", label="net_buy")
    plt.legend()
    plt.show()
