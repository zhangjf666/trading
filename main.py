import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import os

from trading.collector.constant import (stock_basic_file, stock_history_path,
                                        stock_tradedate_file)


# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False

# x = np.linspace(-100, 100, 1000)
# y1 = x.copy()
# y2 = x**2
# y3 = 3 * x**3 + 5 * x**2 + 2 * x + 1
# plt.plot(x, y1, color="red", label="y=x")
# plt.plot(x, y2, color="blue", label="y=x^2")
# plt.plot(x, y3, color="yellow", label="y=3*x^3 + 5*x^2 + 2*x + 1")
# plt.ylim(-1000, 1000)
# plt.xlim(-1000, 1000)
# plt.legend()
# plt.show()

# 画布上面画多个图
# fig = plt.figure()
# ax1 = fig.add_subplot(2, 2, 1)
# ax1.plot([1, 2, 3, 4], [5, 1, 8, 2])
# ax2 = fig.add_subplot(2, 2, 4)
# ax2.plot([1, 2, 3, 4], [2, 3, 7, 1])
# plt.show()

# 5日,30日均线
# df = pd.read_csv(os.path.join(stock_history_path, 'sh600519.csv'))
# df.index = pd.DatetimeIndex(df['date'])
# ma5 = df['close'].rolling(5).mean()
# ma30 = df['close'].rolling(30).mean()
# plt.plot(ma5)
# plt.plot(ma30)
# plt.show()

# 收益曲线
df = pd.read_csv(os.path.join(stock_history_path, 'sh000300.csv'), index_col=0)
df.index = pd.DatetimeIndex(df.index)
df = df['2019-01-01':'2019-12-31']
df['ret'] = df['close']/df['close'].shift(1) - 1 
plt.plot(df.index, df['ret'])
plt.show()
# 收益率
df = df['close']
total_trading_day = len(df.index)
print(total_trading_day)
annual_trading_day = 252
final_net_worth = df.iloc[total_trading_day-1]
print(final_net_worth)
initial_net_worth = df.iloc[0]
print(initial_net_worth)

total_ret_rate = final_net_worth / initial_net_worth - 1
print(total_ret_rate)
annual_ret_rate = pow((final_net_worth / initial_net_worth),
                      (annual_trading_day / total_trading_day)) - 1
print(annual_ret_rate)
