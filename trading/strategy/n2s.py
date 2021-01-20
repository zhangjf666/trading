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


# 收益率计算
def calc_earning_rate(df, field='close'):
    df['net'] = df[field] / df[field].shift(1) - 1
    df.loc[df.index[0], 'net'] = 0
    df['er'] = [round(x, 4) for x in (df['net'] + 1.0).cumprod()]
    print(df['er'])
    er = (df.iloc[-1]['er'] - 1) * 100
    return er


# 计算年化收益率
def calc_annual_revenue_rate(df, field='close', annual_trading_day=250):
    total_trading_day = len(df.index)
    df['net'] = df[field] / df[field].shift(1) - 1
    df.loc[df.index[0], 'net'] = 0
    df['er'] = [round(x, 4) for x in (df['net'] + 1.0).cumprod()]
    final_net_worth = df.iloc[-1]['er']
    initial_net_worth = df.iloc[0]['er']
    annual_ret_rate = pow((final_net_worth / initial_net_worth),
                          (annual_trading_day / total_trading_day)) - 1
    return annual_ret_rate


# 获取北向资金统计数据数据
def get_n2s_data(start_date='2017-01-01',
                 end_date=None,
                 multiple=2,
                 period=252):
    df = pd.read_csv(os.path.join(stock_n2s_path, 'n2s.csv'), encoding='utf-8')
    df.index = pd.DatetimeIndex(df['日期'])
    df = df.sort_index()
    ma252 = df['当日成交净买额'].rolling(period).mean()
    std = df['当日成交净买额'].rolling(period).std()
    up_line = ma252 + multiple * std
    down_line = ma252 - multiple * std
    df['mean'] = ma252
    df['std'] = std
    df['up'] = up_line
    df['down'] = down_line
    if (end_date is None):
        end_date = datetime.datetime.today().strftime("%Y-%m-%d")
    df = df[start_date:end_date]
    return df


# 北向资金买入卖出点位图
def show_n2s_sign(start_date='2017-01-01',
                  end_date=None,
                  multiple=2,
                  period=252):
    # 设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False

    df = get_n2s_data(start_date, end_date, multiple, period)
    # 标记买入卖出点位
    df.loc[df['当日成交净买额'] > df['up'], 'operation'] = 1
    df.loc[df['当日成交净买额'] < df['down'], 'operation'] = 0
    df.loc[df['operation'] == 1, 'buy'] = df['当日成交净买额']
    df.loc[df['operation'] == 0, 'sell'] = df['当日成交净买额']
    # 画图
    plt.plot(df.index, df['up'], color="green", label="up_line")
    plt.plot(df.index, df['down'], color="black", label="down_line")
    plt.plot(df.index, df['当日成交净买额'], color="red", label="net_buy")
    plt.plot(df.index, df['buy'], 'go')
    plt.plot(df.index, df['sell'], 'bo')
    plt.legend()
    plt.show()
