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
import trading.collector.stock_collector as sc

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

today = datetime.datetime.today()
dateStr = today.strftime('%Y-%m-%d')
isTradeDay = sc.is_trade_date(dateStr)
isTradeTime = int(today.strftime('%H%M%S')) - int(datetime.time(9, 30, 0).strftime('%H%M%S')) > 0
if not isTradeDay or not isTradeTime:
    dateStr = sc.next_trade_date(dateStr, offset=-1)
print(dateStr)