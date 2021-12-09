# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 更新板块列表
"""
import trading.collector.stock_collector as sc


if __name__ == '__main__':
    sc.update_concept_board()
    sc.update_industry_board()