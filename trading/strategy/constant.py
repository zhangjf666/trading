"""
Date: 2021-01-14 22:00:56
Desc: 策略数据定义
"""
import os

# csv文件类型
file_type_csv = ".csv"
# 文件保存路径
save_root_path = "./.data/"

strategy_path = os.path.join(save_root_path, "strategy")
if not os.path.exists(strategy_path):
    os.mkdir(strategy_path)  # 如果不存在这个文件夹，就自动创建一个