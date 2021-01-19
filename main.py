import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import os

from trading.collector.constant import (stock_basic_file, stock_history_path,
                                        stock_tradedate_file, stock_n2s_path)

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

np.set_printoptions(threshold=np.inf)
# 若想不以科学计数显示:
np.set_printoptions(suppress=True)

# 5日,30日均线
# df = pd.read_csv(os.path.join(stock_history_path, 'sh600519.csv'))
# df.index = pd.DatetimeIndex(df['date'])
# ma5 = df['close'].rolling(5).mean()
# ma30 = df['close'].rolling(30).mean()
# plt.plot(ma5)
# plt.plot(ma30)
# plt.show()

start_date = '2018-01-01'
end_date = '2018-12-31'
# 生成北向买卖点
n2s = pd.read_csv(os.path.join(stock_n2s_path, 'n2s.csv'), encoding='utf-8')
n2s.index = pd.DatetimeIndex(n2s['日期'])
n2s = n2s.sort_index()
ma252 = n2s['当日成交净买额'].rolling(252).mean()
std = n2s['当日成交净买额'].rolling(252).std()
up_line = ma252 + 2*std
down_line = ma252 - 2*std
n2s['mean'] = ma252
n2s['std'] = std
n2s['up'] = up_line
n2s['down'] = down_line
if(end_date is None):
    end_date = datetime.datetime.today().strftime("%Y-%m-%d")
n2s = n2s[start_date:end_date]
# 标记买入卖出点位
n2s.loc[n2s['当日成交净买额'] > n2s['up'], 'operation'] = 1
n2s.loc[n2s['当日成交净买额'] < n2s['down'], 'operation'] = 0
n2s['position'] = n2s['operation'].shift(1)
n2s['position'].fillna(method='ffill', inplace=True)
n2s['position'].fillna(0, inplace=True)

# 收益曲线
df = pd.read_csv(os.path.join(stock_history_path, 'sh000300.csv'), index_col=0)
df.index = pd.DatetimeIndex(df.index)
df = df[start_date:end_date]
start_worth = df.iloc[0]['close']
df['ret'] = df['close'] / start_worth - 1
n2s = pd.merge(n2s, df, how='inner', left_index=True, right_index=True)
# 计算收益率
n2s.loc[n2s.index, 'c_ret'] = 0
n2s.loc[n2s['position'] > n2s['position'].shift(1), 'c_ret'] = n2s['close']/n2s['open'] - 1
n2s.loc[n2s['position'] < n2s['position'].shift(1), 'c_ret'] = n2s['open']/n2s['close'].shift(1) - 1
n2s.loc[n2s['position'] == n2s['position'].shift(1), 'c_ret'] = n2s['ret'] * n2s['position']

n2s['策略净值'] = [round(x,2) for x in (n2s['c_ret']+1.0).cumprod()]
n2s['指数净值'] = [round(x,2) for x in (n2s['ret']+1.0).cumprod()]

plt.plot(n2s.index, n2s['ret'], color='red', label='ret')
plt.plot(n2s.index, n2s['c_ret'], color='green', label='c_ret')
plt.show()

# 收益曲线
# df = pd.read_csv(os.path.join(stock_history_path, 'sh000300.csv'), index_col=0)
# df.index = pd.DatetimeIndex(df.index)
# df = df[start_date:end_date]
# start_worth = df.iloc[0]['close']
# df['ret'] = df['close'] / start_worth - 1
# plt.plot(df.index, df['ret'])
# plt.show()
# 收益率
# df = df['close']
total_trading_day = len(df.index)
print(total_trading_day)
annual_trading_day = 250
final_net_worth = df.iloc[total_trading_day - 1]['close']
print(final_net_worth)
initial_net_worth = df.iloc[0]['close']
print(initial_net_worth)

total_ret_rate = final_net_worth / initial_net_worth - 1
print(total_ret_rate)
annual_ret_rate = pow((final_net_worth / initial_net_worth),
                      (annual_trading_day / total_trading_day)) - 1
print(annual_ret_rate)

# 计算最大回测
# expanding()计算资金曲线当前的滚动最高值
df['max_close'] = df['close'].expanding().max()
# 计算资金曲线在滚动最高值之后所回撤的百分比
df['per_close'] = df['close'] / df['max_close']
min_point_total = df.sort_values(
    by=['per_close']).iloc[[0], df.columns.get_loc('per_close')]
print(min_point_total)
max_point_total = df[df.index <= min_point_total.index[0]].sort_values(
    by=['close'], ascending=False).iloc[[0], df.columns.get_loc('close')]
print("最大资金回撤%5.2f%%从%s开始至%s结束" %
      ((1 - min_point_total.values), max_point_total.index[0],
       min_point_total.index[0]))
