# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 北向资金分析
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

import trading.collector.constant as cons


# 收益率计算
def calc_earning_rate(df, field='close'):
    tmp = pd.DataFrame(df[field])
    tmp['net'] = tmp[field] / tmp[field].shift(1) - 1
    tmp.loc[df.index[0], 'net'] = 0
    tmp['er'] = [round(x, 4) for x in (tmp['net'] + 1.0).cumprod()]
    er = np.round(((tmp.iloc[-1]['er'] - 1) * 100), 2)
    return er


# 计算年化收益率
def calc_annual_revenue_rate(df, field='close', annual_trading_day=250):
    tmp = pd.DataFrame(df[field])
    total_trading_day = len(df.index)
    tmp['net'] = tmp[field] / tmp[field].shift(1) - 1
    tmp.loc[df.index[0], 'net'] = 0
    tmp['er'] = [round(x, 4) for x in (tmp['net'] + 1.0).cumprod()]
    final_net_worth = tmp.iloc[-1]['er']
    initial_net_worth = tmp.iloc[0]['er']
    annual_ret_rate = round(
        (pow((final_net_worth / initial_net_worth),
             (annual_trading_day / total_trading_day)) - 1) * 100, 2)
    return annual_ret_rate


# 计算最大回撤
def calc_max_drawdown(df, field='close'):
    tmp = pd.DataFrame(df[field])
    # expanding()计算资金曲线当前的滚动最高值
    tmp['max_close'] = tmp[field].expanding().max()
    # 计算资金曲线在滚动最高值之后所回撤的百分比
    tmp['per_close'] = tmp[field] / tmp['max_close']
    min_point_total = tmp.sort_values(
        by=['per_close']).iloc[[0], tmp.columns.get_loc('per_close')]
    return np.round((1 - min_point_total.values[0]) * 100, 2)


# 获取北向资金统计数据数据
def get_n2s_data(start_date='2017-01-01',
                 end_date=None,
                 multiple=2,
                 period=252):
    df = pd.read_csv(os.path.join(cons.stock_n2s_path, 'n2s.csv'),
                     encoding='utf-8')
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
def show_n2s_sign(start_date='2018-01-01',
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
    return df
    # 画图
    # plt.plot(df.index, df['up'], color="green", label="up_line")
    # plt.plot(df.index, df['down'], color="black", label="down_line")
    # plt.plot(df.index, df['当日成交净买额'], color="red", label="net_buy")
    # plt.plot(df.index, df['buy'], 'go')
    # plt.plot(df.index, df['sell'], 'bo')
    # plt.legend()
    # plt.show()


# 北向资金回测产品策略数据
def get_n2s_strategy_data(code,
                            code_type=0,
                          start_date='2017-01-01',
                          end_date=None,
                          multiple=2,
                          period=252):
    if (end_date is None):
        end_date = datetime.datetime.today().strftime("%Y-%m-%d")
    n2s = get_n2s_data(start_date, end_date, multiple, period)
    # 合并指数数据
    if code_type == '0':
        filePath = os.path.join(cons.stock_history_path, code + '.csv')
    elif code_type == '1':
        filePath = os.path.join(cons.index_history_path, code + '.csv')
    df = pd.read_csv(filePath, index_col=0)
    df.index = pd.DatetimeIndex(df.index)
    df = df[start_date:end_date]
    n2s = pd.merge(n2s, df, how='outer', left_index=True, right_index=True)
    # 标记买入卖出点位
    n2s.loc[n2s['当日成交净买额'] > n2s['up'], 'operation'] = 1
    n2s.loc[n2s['当日成交净买额'] < n2s['down'], 'operation'] = 0
    n2s['point'] = n2s['operation'].shift(1)
    n2s['point'].fillna(method='ffill', inplace=True)
    n2s['point'].fillna(0, inplace=True)
    # 计算净值
    n2s['der'] = n2s['收盘'] / n2s['收盘'].shift(1) - 1
    n2s.loc[n2s.index[0], 'der'] = 0
    n2s.loc[n2s.index[0], 's_der'] = 0
    n2s.loc[n2s['point'] > n2s['point'].shift(1),
            's_der'] = n2s['收盘'] / n2s['开盘'] - 1
    n2s.loc[n2s['point'] < n2s['point'].shift(1),
            's_der'] = n2s['开盘'] / n2s['收盘'].shift(1) - 1
    n2s.loc[n2s['point'] == n2s['point'].shift(1),
            's_der'] = n2s['der'] * n2s['point']
    n2s['s_net'] = [round(x, 4) for x in (n2s['s_der'] + 1.0).cumprod()]
    n2s['net'] = [round(x, 4) for x in (n2s['der'] + 1.0).cumprod()]
    return n2s.loc[n2s.index, [
        '代码',
        '名称',
        'operation',
        'point',
        'der',
        'net',
        's_der',
        's_net',
    ]]


"""
1.当日北向资金净买入 > 过去252个交易日的北向资金净买入均值 + 2倍标准差,则第二个交易日全仓买入沪深300
2.当日北向资金净买入 < 过去252个交易日的北向资金净买入均值 - 2倍标准差,则第二个交易日清仓卖出沪深300
3.北向开始时间2016-12-05日, 252个交易日大约一年,最早能开始回测的时间大概在2018-01-01
"""


# 北向资金回测收益率
def get_n2s_strategy_detail(code,
                            code_type='0',
                            start_date='2017-01-01',
                            end_date=None,
                            multiple=2,
                            period=252,
                            annual_trading_day=250):
    if code_type != '0' and code_type != '1':
        raise Exception('代码类型错误')
    n2s = get_n2s_strategy_data(code, code_type, start_date, end_date, multiple, period)
    result = {'code': code, 'name': n2s['名称'].values[0]}
    # 计算收益率
    result['er'] = round((n2s.iloc[-1]['net'] - 1) * 100, 2)
    result['s_er'] = round((n2s.iloc[-1]['s_net'] - 1) * 100, 2)
    # 计算年收益率
    total_trading_day = len(n2s.index)
    final_net_worth = n2s.iloc[-1]['net']
    initial_net_worth = n2s.iloc[0]['net']
    result['arr'] = round(
        (pow((final_net_worth / initial_net_worth),
             (annual_trading_day / total_trading_day)) - 1) * 100, 2)
    final_net_worth = n2s.iloc[-1]['s_net']
    initial_net_worth = n2s.iloc[0]['s_net']
    result['s_arr'] = round(
        (pow((final_net_worth / initial_net_worth),
             (annual_trading_day / total_trading_day)) - 1) * 100, 2)
    # 计算最大回撤
    # expanding()计算资金曲线当前的滚动最高值
    n2s['max_close'] = n2s['net'].expanding().max()
    # 计算资金曲线在滚动最高值之后所回撤的百分比
    n2s['per_close'] = n2s['net'] / n2s['max_close']
    min_point_total = n2s.sort_values(
        by=['per_close']).iloc[[0], n2s.columns.get_loc('per_close')]
    result['min_point'] = min_point_total.index.format()[0]
    max_point_total = n2s[n2s.index <= min_point_total.index[0]].sort_values(
        by=['net'], ascending=False).iloc[[0], n2s.columns.get_loc('net')]
    result['max_point'] = max_point_total.index.format()[0]
    result['max_drawdown'] = round((1 - min_point_total.values[0]) * 100, 2)
    n2s['s_max_net'] = n2s['s_net'].expanding().max()
    n2s['s_per_net'] = n2s['s_net'] / n2s['s_max_net']
    s_min_point_total = n2s.sort_values(
        by=['s_per_net']).iloc[[0], n2s.columns.get_loc('s_per_net')]
    result['s_min_point'] = s_min_point_total.index.format()[0]
    s_max_point_total = n2s[
        n2s.index <= s_min_point_total.index[0]].sort_values(
            by=['s_net'], ascending=False).iloc[[0],
                                                n2s.columns.get_loc('s_net')]
    result['s_max_point'] = s_max_point_total.index.format()[0]
    result['s_max_drawdown'] = round((1 - s_min_point_total.values[0]) * 100, 2)
    n2s.reset_index(inplace=True)
    n2s['日期'] = n2s['日期'].astype(str)
    data = {
        'summary': result,
        'detail': json.loads(n2s.to_json(orient='records'))
    }
    return data


if __name__ == '__main__':
    show_n2s_sign(start_date='2020-01-01')
