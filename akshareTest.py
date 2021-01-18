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
hgt = ak.stock_em_hsgt_hist('沪股通')
hgt = hgt.iloc[:, 0:7]
hgt.to_csv(os.path.join(stock_n2s_path, 'hgt.csv'), encoding="utf-8", index=False)
sgt = ak.stock_em_hsgt_hist('深股通')
sgt = sgt.iloc[:, 0:7]
sgt.to_csv(os.path.join(stock_n2s_path, 'sgt.csv'), encoding="utf-8", index=False)
# 合并北向
pd.to_datetime(hgt['日期'])
hgt = hgt.set_index(['日期'])
pd.to_datetime(sgt['日期'])
sgt = sgt.set_index(['日期'])
n2s = hgt.add(sgt)
n2s = n2s.sort_index(ascending=False)
n2s = n2s.dropna()
n2s = n2s.reset_index()
n2s = n2s.to_csv(os.path.join(stock_n2s_path, 'n2s.csv'), encoding="utf-8", index=False)
