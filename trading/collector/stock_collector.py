# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 股票数据获取
"""

import baostock as bs
import pandas as pd
import os
import akshare as ak
import dateutil
import datetime

import trading.collector.constant as cons


# 登录,退出baostock
def bao_stock_login():
    lg = bs.login()
    if (lg.error_code != '0'):
        raise Exception(lg.error_msg)


def bao_stock_logout():
    bs.logout()


def to_sina_code(code):
    return code[:2] + code[3:]


def from_sina_code(code):
    sl = list(code)
    sl.insert(2, ".")
    return "".join(sl)


# 获取baostock数据
def get_baostock_data(rs):
    if (rs.error_code != '0'):
        raise Exception(rs.error_msg)
    # pandas获取结果集
    result = pd.DataFrame(rs.data, columns=rs.fields)
    return result


# 获取A股票基本资料
def save_stock_basic(code=None, code_name=None):
    """
    获取A股票基本资料
    入参
    code:A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
    code_name:股票名称，支持模糊查询，可以为空。
    返回数据说明
    code	证券代码
    code_name	证券名称
    ipoDate	上市日期
    outDate	退市日期
    type	证券类型，其中1：股票，2：指数,3：其它
    status	上市状态，其中1：上市，0：退市
    """

    if (code is not None):
        code = from_sina_code(code)
    # 获取历史K线数据
    # 详细指标参数，参见“历史行情指标参数”章节
    rs = bs.query_stock_basic(code, code_name)
    result = get_baostock_data(rs)
    result['code'] = result['code'].str[:2] + result['code'].str[3:]
    # 结果集输出到csv文件
    result.to_csv(cons.stock_basic_file, encoding="utf-8", index=False)


# 获取股票历史行情
history_data_filed = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,\
    pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"


def save_history_k_data(code,
                        fields=history_data_filed,
                        start_date=None,
                        end_date=None,
                        frequency='d',
                        adjustflag='3',
                        save_header=True):
    """
    获取A股历史K线数据
    入参
    code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
    fields：指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。详细指标列表见历史行情指标参数章节，日线与分钟线参数不同。此参数不可为空；
    start：开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
    end：结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
    frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
    adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。
    """

    bao_code = from_sina_code(code)
    # 获取历史K线数据
    # 详细指标参数，参见“历史行情指标参数”章节
    rs = bs.query_history_k_data_plus(
        bao_code, fields, start_date, end_date, frequency,
        adjustflag)  # frequency="d"取日k线，adjustflag="3"默认不复权

    result = get_baostock_data(rs)
    result['code'] = result['code'].str[:2] + result['code'].str[3:]
    # 结果集输出到csv文件
    if (not save_header):
        save_header = None
    result.to_csv(os.path.join(cons.stock_history_path, code + ".csv"),
                  encoding="utf-8",
                  index=False,
                  mode='a',
                  header=save_header)


# 保存交易日历
def save_tradeday():
    df = ak.tool_trade_date_hist_sina()
    df.to_csv(cons.stock_tradedate_file, encoding="utf-8", index=False)


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


# 季频资料获取
def collect_quarter_stock_data(code, year, quarter):
    # 合并季频指标
    def merge_data(df, bs_result):
        result = get_baostock_data(bs_result)
        result.set_index("statDate", inplace=True)
        cols_to_use = result.columns.difference(df.columns)
        df = pd.merge(df,
                      result[cols_to_use],
                      how="outer",
                      left_index=True,
                      right_index=True)
        return df

    try:
        # 季频盈利能力
        rs_profit = bs.query_profit_data(code, year, quarter)
        result = get_baostock_data(rs_profit)
        df = result
        df.set_index("statDate", inplace=True)
        # 季频营运能力
        rs = bs.query_operation_data(code, year, quarter)
        df = merge_data(df, rs)
        # 季频成长能力
        rs = bs.query_growth_data(code, year, quarter)
        df = merge_data(df, rs)
        # 季频偿债能力
        rs = bs.query_balance_data(code, year, quarter)
        df = merge_data(df, rs)
        # 季频现金流量
        rs = bs.query_cash_flow_data(code, year, quarter)
        df = merge_data(df, rs)
        # 季频杜邦指数
        rs = bs.query_dupont_data(code, year, quarter)
        df = merge_data(df, rs)
        df.reset_index(inplace=True)
    except Exception as e:
        print(e)
        raise e
    return df


# 季频资料保存
def save_quarter_stock_data(code):
    fname = os.path.join(cons.stock_quarter_path, code + ".csv")
    exists = os.path.exists(fname)
    start_date = datetime.date(2000, 1, 1)
    fdf = None
    if (exists):
        fdf = pd.read_csv(fname)
        fdf.index = pd.DatetimeIndex(fdf["statDate"])
        fdf.sort_index()
        start_date = dateutil.parser.parse(fdf["statDate"].values[-1])
    # 循环获取季频资料
    bao_code = from_sina_code(code)
    now_date = datetime.datetime.now()
    while (start_date.year != now_date.year or
           pd.Timestamp(start_date).quarter != pd.Timestamp(now_date).quarter):
        start_date = start_date + dateutil.relativedelta.relativedelta(
            months=3)
        rs = collect_quarter_stock_data(bao_code, start_date.year,
                                        pd.Timestamp(start_date).quarter)
        if (rs.empty):
            continue
        rs['code'] = rs['code'].str[:2] + rs['code'].str[3:]
        if (fdf is None):
            fdf = rs
        else:
            fdf = pd.concat([fdf, rs])
    # 结果集输出到csv文件
    save_header = True if not exists else None
    fdf.to_csv(fname,
               encoding="utf-8",
               index=False,
               mode='a',
               header=save_header)


# 业绩预告
def save_forecast(date):
    """
    date 注意取值,只能为每季度末日期,例如,2020-03-31,2020-06-30,2020-09-30,2020-12-31
    """
    df = ak.stock_em_yjyg(date)
    df.to_csv(os.path.join(cons.stock_forecast_path, date + cons.file_type_csv), encoding="utf-8", index=False)


if __name__ == '__main__':
    # bao_stock_login()
    save_forecast("2021-03-31")
    # bao_stock_logout()
