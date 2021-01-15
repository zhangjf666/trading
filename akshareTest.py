import akshare as ak
import dateutil.parser
import pandas as pd


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

# 获取交易日历,筛选指定时间的交易日历
t = dateutil.parser.parse("2021-01-01")
df = ak.tool_trade_date_hist_sina()
df['trade_date'] = pd.to_datetime(df['trade_date'])
print(df[df['trade_date'] > t])
