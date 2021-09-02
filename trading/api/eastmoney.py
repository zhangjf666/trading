# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/9/2 22:26
Desc: 东方财富网-数据获取
"""
import requests
import pandas as pd


def stock_zh_a_spot_em() -> pd.DataFrame:
    """
    东方财富-A股-实时行情
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "http://35.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.columns = ["_",
                       "最新价",
                       "涨跌幅",
                       "涨跌额",
                       "成交量",
                       "成交额",
                       "振幅",
                       "换手率",
                       "市盈率-动态",
                       "量比",
                       "_",
                       "代码",
                       "_",
                       "名称",
                       "最高",
                       "最低",
                       "今开",
                       "昨收",
                       "总市值",
                       "流通市值",
                       "_",
                       "市净率",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       "_",
                       ]
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.rename(columns={'index': "序号"}, inplace=True)
    temp_df = temp_df[[
        "序号",
        "代码",
        "名称",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "最高",
        "最低",
        "今开",
        "昨收",
        "量比",
        "换手率",
        "总市值",
        "流通市值",
        "市盈率-动态",
        "市净率",
    ]]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors='coerce')
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors='coerce')
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors='coerce')
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors='coerce')
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors='coerce')
    temp_df['振幅'] = pd.to_numeric(temp_df['振幅'], errors='coerce')
    temp_df['最高'] = pd.to_numeric(temp_df['最高'], errors='coerce')
    temp_df['最低'] = pd.to_numeric(temp_df['最低'], errors='coerce')
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors='coerce')
    temp_df['昨收'] = pd.to_numeric(temp_df['昨收'], errors='coerce')
    temp_df['量比'] = pd.to_numeric(temp_df['量比'], errors='coerce')
    temp_df['换手率'] = pd.to_numeric(temp_df['换手率'], errors='coerce')
    temp_df['总市值'] = pd.to_numeric(temp_df['总市值'], errors='coerce')
    temp_df['流通市值'] = pd.to_numeric(temp_df['流通市值'], errors='coerce')
    temp_df['市盈率-动态'] = pd.to_numeric(temp_df['市盈率-动态'], errors='coerce')
    temp_df['市净率'] = pd.to_numeric(temp_df['市净率'], errors='coerce')
    return temp_df


if __name__ == "__main__":
    stock_zh_a_spot_em_df = stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)
