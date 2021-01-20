# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 策略测试
"""
import pandas as pd
import os
import trading.strategy.n2s as tsn
import trading.collector.constant as cons

# 北向资金买入卖出指数
# tsn.show_n2s_sign(start_date='2020-01-01', period=50)

# 北向资金回测指数
start_date = '2019-01-01'
end_date = '2019-12-31'
code = 'sh000300'
n2s = tsn.get_n2s_data(start_date, end_date)
# 标记买入卖出点位
n2s.loc[n2s['当日成交净买额'] > n2s['up'], 'operation'] = 1
n2s.loc[n2s['当日成交净买额'] < n2s['down'], 'operation'] = 0
n2s['position'] = n2s['operation'].shift(1)
n2s['position'].fillna(method='ffill', inplace=True)
n2s['position'].fillna(0, inplace=True)
# 获取指数数据
df = pd.read_csv(os.path.join(cons.stock_history_path, code + '.csv'), index_col=0)
df.index = pd.DatetimeIndex(df.index)
df = df[start_date:end_date]
df['ret'] = df['close'] / df['close'].shift(1) - 1
df.loc[df.index[0], 'ret'] = 0
print(df['ret'])