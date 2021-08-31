# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 股票数据获取
"""

import pandas as pd
import os
import akshare as ak

import trading.collector.constant as cons


def to_sina_code(code):
    return code[:2] + code[3:]


def from_sina_code(code):
    sl = list(code)
    sl.insert(2, ".")
    return "".join(sl)


# 采集A股票基本资料
def save_stock_basic():
    """
    获取A股票基本资料
    返回数据说明
    code	证券代码
    name	证券名称
    """
    result = ak.stock_zh_a_spot_em()
    result.dropna(inplace=True)
    result = result[['代码', '名称']]
    result.columns = ['code', 'name']
    result.sort_values(by='code', inplace=True)
    # 结果集输出到csv文件
    result.to_csv(cons.stock_basic_file, encoding="utf-8", index=False)


# 获取A股历史K线数据
def save_history_k_data(code,
                        start_date='19800101',
                        end_date='21211231',
                        adjust=""):
    """
    获取A股历史K线数据
    入参
    code：股票代码，6位数字代码，此参数不可为空；
    start_date：开始日期（包含），格式“YYYYMMDD”，为空时取19900101；
    end_date：结束日期（包含），格式“YYYYMMDD”，为空时取最近一个交易日；
    adjust：复权类型，默认不复权,qfq:前复权,hfq:后复权
    """

    file_name = os.path.join(cons.stock_history_path, code + ".csv")
    exists = os.path.exists(file_name)
    start_date = '19800101'
    data = None
    if (exists):
        data = pd.read_csv(file_name)
        data.index = pd.DatetimeIndex(data['日期'])
        data = data.sort_index()
        start_date = data['日期'].values[-1].replace('-', '')
        # 去掉最后一行数据
        data = data[:-1]
        data.reset_index(inplace=True, drop=True)
    result = ak.stock_zh_a_hist(code, start_date, end_date, adjust)
    if(data is not None):
        data = pd.concat([data, result])
    else:
        data = result
    # 结果集输出到csv文件
    data.to_csv(os.path.join(cons.stock_history_path, code + ".csv"), encoding="utf-8", index=False)


# 保存交易日历
def save_tradeday():
    df = ak.tool_trade_date_hist_sina()
    df.to_csv(cons.stock_tradedate_file, encoding="utf-8", index=False)


# 获取某个日期的后一个交易日
def next_trade_date(date):
    tf = pd.read_csv(cons.stock_tradedate_file)
    tf['trade_date'] = pd.to_datetime(tf['trade_date'])
    tf.sort_values('trade_date')
    tf = tf[tf['trade_date'] > date]
    return pd.Timestamp(tf['trade_date'].values[0]).to_pydatetime()


# 检查某个日期是否是交易日
def is_trade_date(date):
    tf = pd.read_csv(cons.stock_tradedate_file)
    return date in tf['trade_date'].values


# 保存北向资金信息
def save_n2s():
    # 北向流入
    hgt = ak.stock_em_hsgt_hist('沪股通')
    hgt = hgt.iloc[:, 0:7]
    hgt.to_csv(os.path.join(cons.stock_n2s_path, 'hgt.csv'),
               encoding="utf-8",
               index=False)
    sgt = ak.stock_em_hsgt_hist('深股通')
    sgt = sgt.iloc[:, 0:7]
    sgt.to_csv(os.path.join(cons.stock_n2s_path, 'sgt.csv'),
               encoding="utf-8",
               index=False)
    # 合并北向
    pd.to_datetime(hgt['日期'])
    hgt = hgt.set_index(['日期'])
    pd.to_datetime(sgt['日期'])
    sgt = sgt.set_index(['日期'])
    n2s = hgt.add(sgt)
    n2s = n2s.sort_index(ascending=False)
    n2s = n2s.dropna()
    n2s = n2s.reset_index()
    n2s = n2s.to_csv(os.path.join(cons.stock_n2s_path, 'n2s.csv'),
                     encoding="utf-8",
                     index=False)


# 业绩预告
def save_forecast(date):
    """
    date 注意取值,只能为每季度末日期,例如,2020-03-31,2020-06-30,2020-09-30,2020-12-31
    """
    df = ak.stock_em_yjyg(date)
    df.to_csv(os.path.join(cons.stock_forecast_path, date + cons.file_type_csv), encoding="utf-8", index=False)


if __name__ == '__main__':
    save_forecast('20210630')
