"""
Date: 2021-01-14 22:00:56
Desc: 普通工具类
"""
import time
import json

from pandas.core.frame import DataFrame


def sleep(secend: int = 1):
    time.sleep(secend)


# dataframe转为数据转为json,由于直接转json列名会按字母顺序排列,无法保持列原来的顺序
# 所以整合一下多输出一个列名数组
def to_json(df: DataFrame):
    if df.shape[0] <= 0:
        return {'columns': [], 'data': []}
    else:
        return {'columns': df.columns.values.tolist(), 'data': json.loads(df.to_json(orient='records'))}
