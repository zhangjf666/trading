# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 策略测试
"""
import pandas as pd
import os
import trading.strategy.n2s
import trading.strategy.n2s as tsn
import trading.collector.constant as cons
import matplotlib.pyplot as plt

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False

# 北向资金买入卖出指数
# tsn.show_n2s_sign(start_date='2020-01-01')

start_date = '2021-12-01'
end_date = '2021-12-31'
code = '600519'
# 北向资金回测指数数据图表
# n2s = tsn.get_n2s_strategy_data(code, start_date, end_date)
# fig, ax1 = plt.subplots()
# ax1.set_title(code)
# ax1.plot(n2s.index, n2s['s_net'], color='red', label='策略净值')
# ax1.plot(n2s.index, n2s['net'], color='green', label='指数净值')
# ax1.set_ylim(n2s['s_net'].min() * 0.9, n2s['s_net'].max() * 1.1)
# ax2 = ax1.twinx()
# ax2.plot(n2s.index, n2s['point'], color='blue', label='买卖点')
# ax1.legend()
# ax2.legend()
# plt.show()
# 北向资金回测指数总计
n2s = tsn.get_n2s_strategy_detail(code=code, code_type='0', start_date=start_date, end_date=end_date)
print(n2s)
