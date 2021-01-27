# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 基金数据获取
"""

import pandas as pd
import os
import akshare as ak

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


if __name__ == '__main__':
    save_exchange_rank()
