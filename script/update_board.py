# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 更新板块列表
"""
import sys
import datetime
import trading.collector.stock_collector as sc


if __name__ == '__main__':
    start_year = datetime.datetime.now().year
    end_year = datetime.datetime.now().year
    if len(sys.argv) >= 2:
        start_year = sys.argv[1]
    if len(sys.argv) >= 3:
        end_year = sys.argv[2]
    sc.update_concept_board()
    sc.update_industry_board()
    sc.update_concept_stocks()
    sc.update_industry_stocks()
    sc.update_all_concept_index(start_year, end_year)
    sc.update_all_industry_index(start_year, end_year)
