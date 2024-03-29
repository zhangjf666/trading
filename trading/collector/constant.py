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

# 股票文件夹
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

# 板块文件夹
board_path = os.path.join(stock_path, 'board')
# 如果文件夹不存在,先创建
fileUtil.createPath(board_path)
# 概念板块列表文件名
concept_list_file_name = "concept_list.csv"
# 概念板块列表文件
concept_list_file = os.path.join(board_path, concept_list_file_name)
# 概念板块成分股文件名
concept_stocks_file_name = "concept_stock.csv"
# 概念板块成分股文件
concept_stocks_file = os.path.join(board_path, concept_stocks_file_name)
# 概念板块指数文件夹
concept_index_path = os.path.join(board_path, "concept_index")
fileUtil.createPath(concept_index_path)
# 行业板块列表文件名
industry_list_file_name = "industry_list.csv"
# 行业板块列表文件
industry_list_file = os.path.join(board_path, industry_list_file_name)
# 行业板块成分股文件名
industry_stocks_file_name = "industry_stock.csv"
# 行业板块成分股文件
industry_stocks_file = os.path.join(board_path, industry_stocks_file_name)
# 行业板块指数文件夹
industry_index_path = os.path.join(board_path, "industry_index")
fileUtil.createPath(industry_index_path)
# 债券文件夹
bond_path = os.path.join(stock_path, 'bond')
fileUtil.createPath(bond_path)
# 可转债比价表文件名
convertible_file_name = "convertible.csv"
# 可装在比价表文件
convertible_file = os.path.join(bond_path, convertible_file_name)
# 指数文件夹
index_path = os.path.join(stock_path, 'index')
# 如果文件夹不存在,先创建
fileUtil.createPath(index_path)
# 指数列表文件名
index_list_file_name = "index_list.csv"
# 指数列表文件
index_list_file = os.path.join(index_path, index_list_file_name)
# 指数分股文件名
index_stocks_file_name = "index_stock.csv"
# 指数成分股文件
index_stocks_file = os.path.join(index_path, index_stocks_file_name)
# 概念板块指数文件夹
index_history_path = os.path.join(index_path, "index_history")
fileUtil.createPath(index_history_path)

# 机构调研统计文件名
jgdytj_file_name = "jgdytj.csv"
# 机构调研统计文件
jgdytj_file = os.path.join(stock_path, jgdytj_file_name)

# 技术指标文件夹
jszb_path = os.path.join(stock_path, "jszb")
fileUtil.createPath(jszb_path)
# 创新高文件名
cxg_file_name = "cxg.csv"
# 创新高文件
cxg_file = os.path.join(jszb_path, cxg_file_name)
# 创新低文件名
cxd_file_name = "cxd.csv"
# 创新低文件
cxd_file = os.path.join(jszb_path, cxd_file_name)
# 连续上涨文件名
lxsz_file_name = "lxsz.csv"
# 连续上涨文件
lxsz_file = os.path.join(jszb_path, lxsz_file_name)
# 连续下跌文件名
lxxd_file_name = "lxxd.csv"
# 连续下跌文件
lxxd_file = os.path.join(jszb_path, lxxd_file_name)
# 持续放量文件名
cxfl_file_name = "cxfl.csv"
# 持续放量文件
cxfl_file = os.path.join(jszb_path, cxfl_file_name)
# 持续缩量文件名
cxsl_file_name = "cxsl.csv"
# 持续缩量文件
cxsl_file = os.path.join(jszb_path, cxsl_file_name)
# 量价齐升文件名
ljqs_file_name = "ljqs.csv"
# 量价齐升文件
ljqs_file = os.path.join(jszb_path, ljqs_file_name)
# 量价齐跌文件名
ljqd_file_name = "ljqd.csv"
# 量价齐跌文件
ljqd_file = os.path.join(jszb_path, ljqd_file_name)

# 资金流向文件夹
zjlx_path = os.path.join(stock_path, "zjxl")
fileUtil.createPath(zjlx_path)

# 外汇文件夹
forex_path = os.path.join(save_root_path, "forex")
# 如果文件夹不存在,先创建
fileUtil.createPath(forex_path)

forex_history_path = os.path.join(forex_path, "history")
# 如果文件夹不存在,先创建
fileUtil.createPath(forex_history_path)

forex_basic_file_name = "forex_basic.csv"

forex_basic_file = os.path.join(forex_path, forex_basic_file_name)
