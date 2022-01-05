# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/9/2 22:26
Desc: 通用数据获取(各种来源)
"""
import requests
import pandas as pd
from io import BytesIO


def index_stock_cons_csindex(index: str = "000300") -> pd.DataFrame:
    """
    最新股票指数的成份股目录-中证指数网站
    http://www.csindex.com.cn/zh-CN/indices/index-detail/000300
    :param index: 指数代码, 可以通过 index_stock_info 函数获取
    :type index: str
    :return: 最新股票指数的成份股目录
    :rtype: pandas.DataFrame
    """
    url = f"https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/cons/{index}cons.xls"
    r = requests.get(url)
    temp_df = pd.read_excel(BytesIO(r.content))
    if '沪市代码Constituent Code SHH' in temp_df.columns and '沪市名称Constituent Name SHH' in temp_df.columns:
        temp_df = temp_df[['沪市代码Constituent Code SHH', '沪市名称Constituent Name SHH']]
    elif '成分券代码Constituent Code' in temp_df.columns and '成分券名称Constituent Name' in temp_df.columns:
        temp_df = temp_df[['成分券代码Constituent Code', '成分券名称Constituent Name']]
    temp_df.columns = ["代码", "名称"]
    temp_df['代码'] = temp_df['代码'].astype(str).str.zfill(6)
    temp_df.dropna(inplace=True)
    return temp_df
