# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 公共计算方法
"""

import numpy as np
import pandas as pd


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


# 计算最大回撤并返回对应日期
def calc_max_drawdown_detail(df, field='close'):
    tmp = pd.DataFrame(df[field])
    # expanding()计算资金曲线当前的滚动最高值
    tmp['max_close'] = tmp[field].expanding().max()
    # 计算资金曲线在滚动最高值之后所回撤的百分比
    tmp['per_close'] = tmp[field] / tmp['max_close']
    min_point_total = tmp.sort_values(
        by=['per_close']).iloc[[0], tmp.columns.get_loc('per_close')]
    max_point_total = tmp[tmp.index <= min_point_total.index[0]].sort_values(
        by=['per_close'], ascending=False).iloc[[0], tmp.columns.get_loc('per_close')]
    max_drawdown = np.round((1 - min_point_total.values[0]) * 100, 2)
    return {'max_date': max_point_total.index.date[0].strftime('%Y-%m-%d'), 'min_date':min_point_total.index.date[0].strftime('%Y-%m-%d'), 'max_drawdown': max_drawdown}