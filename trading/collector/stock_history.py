# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021-01-14 22:00:56
Desc: 股票历史数据获取
"""

import baostock as bs
import pandas as pd
import os

from trading.collector.constant import (collector_save_path)


def query_history_k_data(code,
                         fields,
                         start_date=None,
                         end_date=None,
                         frequency='d',
                         adjustflag='3'):
    lg = bs.login()

    # 获取历史K线数据
    # 详细指标参数，参见“历史行情指标参数”章节
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
        start_date,
        end_date,
        frequency,
        adjustflag)  # frequency="d"取日k线，adjustflag="3"默认不复权

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_csv(os.path.join(collector_save_path, code + ".csv"),
                  encoding="gbk",
                  index=False)
    print(result)

    # 登出系统
    bs.logout()


if __name__ == '__main__':
    df = query_history_k_data("sh.600519", "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST","2019-01-01", "2019-12-31")
