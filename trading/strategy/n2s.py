# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 北向资金分析
"""


"""
1.当日北向资金净买入 > 过去252个交易日的北向资金净买入均值 + 2倍标准差,则第二个交易日全仓买入沪深300
2.当日北向资金净买入 < 过去252个交易日的北向资金净买入均值 - 2倍标准差,则第二个交易日清仓卖出沪深300
3.北向开始时间2016-12-05日, 252个交易日大约一年,最早能开始回测的时间大概在2018-01-01
"""