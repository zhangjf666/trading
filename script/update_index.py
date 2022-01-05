# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 更新指数相关
"""
import trading.collector.stock_collector as sc


if __name__ == '__main__':
    sc.update_index()
    sc.update_index_daily()
    sc.update_index_stocks()