import akshare as ak
import dateutil.parser
import pandas as pd
import trading.collector.stock_collector as sc
import os

from trading.collector.constant import (stock_n2s_path)

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

# 保存交易日历
# sc.save_tradeday()

# 北向流入
sc.save_n2s()
