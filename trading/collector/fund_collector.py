# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 基金数据获取
"""

import pandas as pd
import os
import akshare as ak
import datetime
import demjson
import requests
from lxml import etree
import trading.collector.constant as cons


# 获取基金基本信息
def save_fund_basic():
    df = ak.fund_em_fund_name()
    df.to_csv(cons.fund_basic_file, encoding="utf-8", index=False)


# 开放式基金排行
def save_open_fund_rank():
    df = ak.fund_em_open_fund_rank()
    df.to_csv(cons.fund_open_fund_rank_file, encoding="utf-8", index=False)


# 场内交易基金排行
def save_exchange_rank():
    df = ak.fund_em_exchange_rank()
    df.to_csv(cons.fund_exchange_rank_file, encoding="utf-8", index=False)


# 基金最新十大持股
def sava_stock_hold(code, year=None):
    if (code is None):
        raise Exception("基金代码不能为空")
    if (year is None):
        # 如果是一季度或者5月份之前,取上一年的数据
        today = datetime.datetime.today()
        quarter = pd.Timestamp(today).quarter
        if (quarter == 1 or today.month < 5):
            year = today.year - 1
        else:
            year = today.year
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "jjcc",
        "code": code,
        "topline": "10",
        "year": year,
        "month": ""
    }
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fundf10.eastmoney.com/ccmx_" + code + ".html",
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = demjson.decode(text_data[text_data.find("{"):-1])
    content = json_data["content"]
    if (len(content) == 0):
        print(code + ":获取持股内容为空")
        return
    html = etree.HTML(content)
    tb_list = html.xpath('//table')
    tr_list = tb_list[0].xpath('tbody/tr')
    stock_list = []

    for tr in tr_list:
        td_list = tr.xpath('td')
        stock = []
        # 顺序
        stock.append(td_list[0].text)
        # 代码
        elec = td_list[1].xpath('a')
        if(len(elec) == 0):
            elec = td_list[1].xpath('span')
            if(len(elec) == 0):
                elec = td_list[1]
        stock.append(elec[0].text)
        # 名称
        elen = td_list[2].xpath('a')
        if(len(elen) == 0):
            elen = td_list[2].xpath('span')
            if(len(elen) == 0):
                elen = td_list[2]
        stock.append(elen[0].text)
        # 占净值比例
        stock.append(td_list[-3].text)
        # 持股数(万股)
        stock.append(td_list[-2].text)
        # 持仓市值(万元)
        stock.append(td_list[-1].text)
        stock_list.append(stock)
    df = pd.DataFrame(stock_list)
    df.columns = ["序号", "股票代码", "股票名称", "占净值比例", "持股数", "持仓市值"]
    df.to_csv(os.path.join(cons.fund_stock_hold_path, code + ".csv"),
              encoding="utf-8",
              index=False)


if __name__ == '__main__':
    sava_stock_hold('009791')
