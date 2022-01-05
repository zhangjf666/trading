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

from akshare.index.cons import (
    zh_sina_index_stock_payload,
    zh_sina_index_stock_url,
    zh_sina_index_stock_count_url,
    zh_sina_index_stock_hist_url,
)
from akshare.stock.cons import hk_js_decode


# 设置重试次数
requests.adapters.DEFAULT_RETRIES = 3


def _sleep(secend: int = 1):
    time.sleep(secend)


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


def stock_zh_index_daily(symbol: str = "sh000922") -> pd.DataFrame:
    """
    新浪财经-指数-历史行情数据, 大量抓取容易封IP
    https://finance.sina.com.cn/realstock/company/sh000909/nc.shtml
    :param symbol: sz399998, 指定指数代码
    :type symbol: str
    :return: 历史行情数据
    :rtype: pandas.DataFrame
    """
    params = {"d": "2020_2_4"}
    res = requests.get(zh_sina_index_stock_hist_url.format(symbol), params=params)
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    temp_df = pd.DataFrame(dict_list)
    temp_df['date'] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df['open'] = pd.to_numeric(temp_df['open'])
    temp_df['close'] = pd.to_numeric(temp_df['close'])
    temp_df['high'] = pd.to_numeric(temp_df['high'])
    temp_df['low'] = pd.to_numeric(temp_df['low'])
    temp_df['volume'] = pd.to_numeric(temp_df['volume'])
    return temp_df


def index_stock_cons(index: str = "399639") -> pd.DataFrame:
    """
    最新股票指数的成份股目录
    http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=1&indexid=399639
    :param index: 指数代码, 可以通过 index_stock_info 函数获取
    :type index: str
    :return: 最新股票指数的成份股目录
    :rtype: pandas.DataFrame
    """
    url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/{index}.phtml"
    r = requests.get(url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    page_num = (
        soup.find(attrs={"class": "table2"})
        .find("td")
        .find_all("a")[-1]["href"]
        .split("page=")[-1]
        .split("&")[0]
    )
    if page_num == "#":
        temp_df = pd.read_html(r.text, header=1)[3].iloc[:, :3]
        temp_df["品种代码"] = temp_df["品种代码"].astype(str).str.zfill(6)
        return temp_df

    temp_df = pd.DataFrame()
    for page in range(1, int(page_num) + 1):
        url = f"http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page={page}&indexid={index}"
        r = requests.get(url)
        r.encoding = "gb2312"
        temp_df = temp_df.append(pd.read_html(r.text, header=1)[3], ignore_index=True)
        _sleep()
    temp_df = temp_df.iloc[:, :3]
    temp_df["品种代码"] = temp_df["品种代码"].astype(str).str.zfill(6)
    return temp_df
