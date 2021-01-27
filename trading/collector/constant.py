# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 数据获取定义
"""
import os

# 文件保存路径
save_root_path = "./.data/"

stock_path = os.path.join(save_root_path, "stock")

stock_history_path = os.path.join(stock_path, "history")

stock_basic_file_name = "stock_basic.csv"

stock_basic_file = os.path.join(stock_path, stock_basic_file_name)

stock_tradedate_file_name = "stock_tradedate.csv"

stock_tradedate_file = os.path.join(stock_path, stock_tradedate_file_name)

stock_n2s_path = os.path.join(stock_path, "n2s")

fund_path = os.path.join(save_root_path, "fund")

fund_basic_file_name = "fund_basic.csv"

fund_basic_file = os.path.join(fund_path, fund_basic_file_name)

fund_open_fund_rank_file_name = "open_fund_rank.csv"

fund_open_fund_rank_file = os.path.join(fund_path, fund_open_fund_rank_file_name)

fund_exchange_rank_file_name = "exchange_rank.csv"

fund_exchange_rank_file = os.path.join(fund_path, fund_exchange_rank_file_name)

