import akshare as ak
import dateutil.parser
import pandas as pd
import trading.collector.stock_collector as sc
import os

from trading.collector.constant import (save_root_path)

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

# 保存交易日历
# sc.save_tradeday()

# 北向流入
# hdf = ak.stock_em_hsgt_hist('沪股通')
# hdf.to_csv(os.path.join(save_root_path,'hgt.csv'))
# sdf = ak.stock_em_hsgt_hist('深股通')
# sdf.to_csv(os.path.join(save_root_path,'sgt.csv'))
# 合并北向
hdf = pd.read_csv(os.path.join(save_root_path, 'hgt.csv'))
sdf = pd.read_csv(os.path.join(save_root_path, 'sgt.csv'))
hdf.index = pd.DatetimeIndex(hdf['日期'])
sdf.index = pd.DatetimeIndex(sdf['日期'])
tdf = hdf.iloc[:, 0:8] + sdf.iloc[:, 0:8]
tdf = tdf.to_csv(os.path.join(save_root_path, 'total.csv'))
