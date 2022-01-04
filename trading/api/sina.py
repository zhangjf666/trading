# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/9/2 22:26
Desc: 新浪-数据获取
"""
import re
import os
import time
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm
import demjson

# 设置重试次数
requests.adapters.DEFAULT_RETRIES = 3


def _sleep(secend: int = 1):
    time.sleep(secend)

zh_sina_index_stock_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple"
zh_sina_index_stock_payload = {
    "page": "1",
    "num": "80",
    "sort": "symbol",
    "asc": "1",
    "node": "hs_s",
    "_s_r_a": "page"
}
zh_sina_index_stock_count_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCountSimple?node=hs_s"
zh_sina_index_stock_hist_url = "https://finance.sina.com.cn/realstock/company/{}/hisdata/klc_kl.js"


def _replace_comma(x):
    """
    去除单元格中的 ","
    :param x: 单元格元素
    :type x: str
    :return: 处理后的值或原值
    :rtype: str
    """
    if ',' in str(x):
        return str(x).replace(",", "")
    else:
        return x


def get_zh_index_page_count() -> int:
    """
    指数的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_s
    :return: 需要抓取的指数的总页数
    :rtype: int
    """
    res = requests.get(zh_sina_index_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_index_spot() -> pd.DataFrame:
    """
    新浪财经-指数
    大量采集会被目标网站服务器封禁 IP
    http://vip.stock.finance.sina.com.cn/mkt/#hs_s
    :return: 所有指数的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_zh_index_page_count()
    zh_sina_stock_payload_copy = zh_sina_index_stock_payload.copy()
    for page in tqdm(range(1, page_count + 1)):
        zh_sina_stock_payload_copy.update({"page": page})
        res = requests.get(zh_sina_index_stock_url, params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
        _sleep()
    big_df = big_df.applymap(_replace_comma)
    big_df["trade"] = big_df["trade"].astype(float)
    big_df["pricechange"] = big_df["pricechange"].astype(float)
    big_df["changepercent"] = big_df["changepercent"].astype(float)
    big_df["buy"] = big_df["buy"].astype(float)
    big_df["sell"] = big_df["sell"].astype(float)
    big_df["settlement"] = big_df["settlement"].astype(float)
    big_df["open"] = big_df["open"].astype(float)
    big_df["high"] = big_df["high"].astype(float)
    big_df["low"] = big_df["low"].astype(float)
    big_df["low"] = big_df["low"].astype(float)
    big_df.columns = [
        '代码',
        '名称',
        '最新价',
        '涨跌额',
        '涨跌幅',
        '_',
        '_',
        '昨收',
        '今开',
        '最高',
        '最低',
        '成交量',
        '成交额',
        '_',
        '_',
    ]
    big_df = big_df[
        [
            '代码',
            '名称',
            '最新价',
            '涨跌额',
            '涨跌幅',
            '昨收',
            '今开',
            '最高',
            '最低',
            '成交量',
            '成交额',
        ]
    ]
    return big_df