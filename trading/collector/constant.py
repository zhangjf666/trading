# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 数据获取定义
"""
import os
import trading.util.file_util as fileUtil

# csv文件类型
file_type_csv = ".csv"
# 文件保存路径
save_root_path = "/python/data/trading/data/"
# 如果文件夹不存在,先创建
fileUtil.createPath(save_root_path)

stock_path = os.path.join(save_root_path, "stock")
# 如果文件夹不存在,先创建
fileUtil.createPath(stock_path)

stock_history_path = os.path.join(stock_path, "history")
# 如果文件夹不存在,先创建
fileUtil.createPath(stock_history_path)

stock_basic_file_name = "stock_basic.csv"

stock_basic_file = os.path.join(stock_path, stock_basic_file_name)

stock_tradedate_file_name = "stock_tradedate.csv"

stock_tradedate_file = os.path.join(stock_path, stock_tradedate_file_name)

stock_n2s_path = os.path.join(stock_path, "n2s")
# 如果文件夹不存在,先创建
fileUtil.createPath(stock_n2s_path)

stock_quarter_path = os.path.join(stock_path, "quarter")
# 如果文件夹不存在,先创建
fileUtil.createPath(stock_quarter_path)

stock_forecast_path = os.path.join(stock_path, "forecast")
# 如果文件夹不存在,先创建
fileUtil.createPath(stock_forecast_path)

fund_path = os.path.join(save_root_path, "fund")
# 如果文件夹不存在,先创建
fileUtil.createPath(fund_path)

fund_basic_file_name = "fund_basic.csv"

fund_basic_file = os.path.join(fund_path, fund_basic_file_name)

fund_open_fund_rank_file_name = "open_fund_rank.csv"

fund_open_fund_rank_file = os.path.join(fund_path, fund_open_fund_rank_file_name)

fund_exchange_rank_file_name = "exchange_rank.csv"

fund_exchange_rank_file = os.path.join(fund_path, fund_exchange_rank_file_name)

fund_stock_hold_path = os.path.join(fund_path, "stock_hold")
# 如果文件夹不存在,先创建
fileUtil.createPath(fund_stock_hold_path)
