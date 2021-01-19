# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 策略测试
"""

import trading.strategy.n2s as tsn

# 北向资金买入卖出指数
tsn.show_n2s_sign(start_date='2018-01-01', end_date='2018-12-31')
