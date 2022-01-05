import os
import datetime
import akshare as ak
from numpy.lib.arraysetops import isin
import pandas as pd
import trading.strategy.calc as scalc
import trading.collector.constant as ccons
import trading.strategy.constant as scons
import trading.api.ths as ths
import trading.api.eastmoney as em
import trading.api.sina as sina
import trading.api.common as capi
import trading.collector.stock_collector as sc

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

df = capi.index_stock_cons_csindex('000013')
print(df)