import akshare as ak
import dateutil.parser
import pandas as pd
import trading.collector.stock_collector as sc
import trading.collector.fund_collector as fc
import os

import trading.collector.constant as cons

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

# 保存交易日历
# sc.save_tradeday()

# 北向流入
sc.save_n2s()

# 获取所有基金十大重仓
# fund_list = pd.read_csv(cons.fund_basic_file, dtype={'基金代码': str})
# for code in fund_list['基金代码']:
#     fc.sava_stock_hold(code)
