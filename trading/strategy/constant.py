"""
Date: 2021-01-14 22:00:56
Desc: 策略数据定义
"""
import os


def createPath(path):
    if not os.path.exists(strategy_path):
        os.makedirs(strategy_path)  # 如果不存在这个文件夹，就自动创建一个


# csv文件类型
file_type_csv = ".csv"
# 文件保存路径
save_root_path = "/python/data/trading/data/"

strategy_path = os.path.join(save_root_path, "strategy")
createPath(strategy_path)

# 超跌次新股搏反弹策略 文件夹
over_sold_new_stock_path = os.path.join(strategy_path, 'over_sold_new_stock')
createPath(over_sold_new_stock_path)

# 均线多头策略 文件夹
ma_higher_path = os.path.join(strategy_path, 'ma_higher')
createPath(ma_higher_path)