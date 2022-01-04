import os
import akshare as ak
from numpy.lib.arraysetops import isin
import pandas as pd
import trading.strategy.calc as scalc
import trading.collector.constant as ccons
import trading.strategy.constant as scons
import trading.api.ths as ths
import trading.api.eastmoney as em

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

# df = ak.stock_zh_index_spot()
df = ak.stock_zh_index_daily('sz399006')
# df = ak.index_stock_cons('000912')
print(df)