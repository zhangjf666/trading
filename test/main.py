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

result = pd.DataFrame()
df = pd.read_csv(scons.ma_higher_stock_file, dtype={'代码': str})
ind_df = pd.read_csv(ccons.industry_stocks_file, dtype={'行业代码': str, '代码': str})
codes = ['881165', '881163']
ind_df = ind_df[ind_df['行业代码'].isin(codes)]
result = result.append(df[df['代码'].isin(ind_df['代码'])])

con_df = pd.read_csv(ccons.concept_stocks_file, dtype={'概念代码': str, '代码': str})
ccodes = ['308733', '308300']
con_df = con_df[con_df['概念代码'].isin(ccodes)]
result = result.append(df[df['代码'].isin(con_df['代码'])])

result.sort_values(by=['持续天数', '流通市值'], ascending=[0, 0], inplace=True)
result = result[(result['持续天数'] >= 1) & (result['持续天数'] <= 65535)]
result = result[result['流通市值'] >= 1 * 100000000]
print(result)