import os
import akshare as ak
import pandas as pd
import trading.strategy.calc as scalc
import trading.collector.constant as conss

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

df = pd.read_csv(os.path.join(conss.stock_history_path, '000001.csv'))
df.index = pd.DatetimeIndex(df['日期'])
scalc.df_ma(df, field='收盘')
print(df[-3:-1])