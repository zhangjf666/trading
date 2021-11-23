"""
Date: 2021-01-14 22:00:56
Desc: 文件工具类
"""
import os


# 如果不存在这个文件夹，就自动创建一个
def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
