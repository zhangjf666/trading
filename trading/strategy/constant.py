"""
Date: 2021-01-14 22:00:56
Desc: 策略数据定义
"""
import os
import trading.util.file_util as fileUtil


# csv文件类型
file_type_csv = ".csv"
# 文件保存路径
save_root_path = "/python/data/trading/data/"

strategy_path = os.path.join(save_root_path, "strategy")
fileUtil.createPath(strategy_path)

# 超跌次新股搏反弹策略 文件夹
over_sold_new_stock_path = os.path.join(strategy_path, 'over_sold_new_stock')
fileUtil.createPath(over_sold_new_stock_path)

# 均线多头策略 文件夹
ma_higher_path = os.path.join(strategy_path, 'ma_higher')
fileUtil.createPath(ma_higher_path)
