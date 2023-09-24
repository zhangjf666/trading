# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 公共计算方法
"""

import talib
import math
import numpy as np
import pandas as pd


# 计算最大回撤
def calc_max_drawdown(df, field='close'):
    tmp = pd.DataFrame(df[field])
    # expanding()计算资金曲线当前的滚动最高值
    tmp['max_close'] = tmp[field].expanding().max()
    # 计算资金曲线在滚动最高值之后所回撤的百分比
    tmp['per_close'] = tmp[field] / tmp['max_close']
    # 去除Nan和inf的影响
    tmp = tmp[~tmp.isin([np.nan, np.inf, -np.inf]).any(1)]
    min_point_total = tmp.sort_values(
        by=['per_close']).iloc[[0], tmp.columns.get_loc('per_close')]
    return np.round((1 - min_point_total.values[0]) * 100, 2)


# 计算最大回撤并返回对应日期
def calc_max_drawdown_detail(df, field='close'):
    tmp = pd.DataFrame(df[field])
    # expanding()计算资金曲线当前的滚动最高值
    tmp['max_close'] = tmp[field].expanding().max()
    # 计算资金曲线在滚动最高值之后所回撤的百分比
    tmp['per_close'] = tmp[field] / tmp['max_close']
    # 去除Nan和inf的影响
    tmp = tmp[~tmp.isin([np.nan, np.inf, -np.inf]).any(1)]
    min_point_total = tmp.sort_values(
        by=['per_close']).iloc[[0], tmp.columns.get_loc('per_close')]
    max_point_total = tmp[tmp.index <= min_point_total.index[0]].sort_values(
        by=[field], ascending=False).iloc[[0], tmp.columns.get_loc(field)]
    max_drawdown = np.round((1 - min_point_total.values[0]) * 100, 2)
    return {'max_date': max_point_total.index.date[0].strftime('%Y-%m-%d'), 'min_date': min_point_total.index.date[0].strftime('%Y-%m-%d'), 'max_drawdown': max_drawdown}


# 计算均线数组
def moving_average(array, n):
    """
    array为每日收盘价组成的数组
    n可以为任意正整数，按照股市习惯，一般设为5或10或20、30、60等
    """
    mov = np.cumsum(array, dtype=float)
    mov[n:] = mov[n:]-mov[:-n]
    moving = mov[(n-1):]/n
    return moving


# dataframe 计算均线数据
def df_ma(df, field='close', ma_list=[5, 10, 20]):
    """
    df: dataframe数据
    field: 需要计算的数据列
    ma_list: 需要的均线列表,默认 5,10,20日均线
    """
    # 按照时间顺序升序排列
    df.sort_index(inplace=True)
    for ma in ma_list:
        df['ma_' + str(ma)] = df[field].rolling(ma).mean()


# dataframe 计算EMA数据
def df_ema(df, field='close', ma_list=[5, 10, 20]):
    """
    df: dataframe数据
    field: 需要计算的数据列
    ma_list: 需要的均线列表,默认 5,10,20日均线
    """
    # 按照时间顺序升序排列
    df.sort_index(inplace=True)
    for ma in ma_list:
        df['ema_' + str(ma)] = talib.EMA(df[field], timeperiod=ma)


# dataframe 计算布林带
def df_bolling(df, field='close', std=2, ma=20):
    """
    df: dataframe数据
    field: 需要计算的数据列
    std: 标准差
    ma: 计算标准差的均线
    """
    df.sort_index(inplace=True)
    df['std'] = df[field].rolling(ma).std(ddof=0)
    df['ma_' + str(ma)] = df[field].rolling(ma).mean()
    df['higher_bound'] = df['ma_'+str(ma)] + 2*df['std']
    df['lower_bound'] = df['ma_'+str(ma)] - 2*df['std']


# 计算某个日期区间涨幅和涨速
def get_slope(price_a, price_b, days):
    rise = (float(price_b) - float(price_a))/float(price_a)
    speed = rise/days
    return {'range': rise * 100, 'speed': speed * 100}


# 计算连续数据出现的最大次数
def calc_field_value_times(data_pd, field, value):
    """
    计算连续数据出现的最大次数
    :param data_pd: 要处理的pandas数据集
    :param field: 要计算的字段
    :param value: 值
    :return:
    """
    # 判断值是否存在
    if data_pd.query("%s == %s" % (field, value)).empty:
        return 0

    data_pd["subgroup"] = data_pd[field].ne(data_pd[field].shift()).cumsum()
    return data_pd.groupby([field, "subgroup"]).apply(len)[value].max()


# 判断是否均线多头,空头排列
def calc_ma_sequence(row, ma_list=[], ma_type='ma'):
    """
    判断是否均线多头,空头排列,返回-1:空头排列,1:多头排列
    入参
    row:带有均线信息的行
    ma_type:均线类型,ma:简单移动平均线,ema:指数平滑移动平均线
    ma_list:所使用的均线列表
    """
    ma_values = []
    for ma in ma_list:
        if math.isnan(row[ma_type + '_' + str(ma)]):
            return 0
        ma_values.append(row[ma_type + '_' + str(ma)])
    if ma_values == sorted(ma_values):
        return -1
    elif ma_values == sorted(ma_values, reverse=True):
        return 1
    return 0
