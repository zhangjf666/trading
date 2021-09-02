import akshare as ak
import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

df = ak.stock_zh_a_spot_em()
# print(df)