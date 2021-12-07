import os
import akshare as ak
import pandas as pd
import trading.strategy.calc as scalc
import trading.collector.constant as conss
import trading.api.ths as ths

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

df = ths.stock_board_industry_index_ths()
print(df)