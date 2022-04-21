"""
Date: 2021-01-14 22:00:56
Desc: 文件工具类
"""
import os


# 如果不存在这个文件夹，就自动创建一个
def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 将替换的字符串写到一个新的文件中
def alterNew(file, new_file, old_str, new_str):
    """
    将替换的字符串写到一个新的文件中
    :param file: 文件路径
    :param new_file: 新文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r", encoding="utf-8") as f1,open(new_file, "w", encoding="utf-8") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
