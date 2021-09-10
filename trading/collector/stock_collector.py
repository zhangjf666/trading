# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 股票数据获取
"""

import pandas as pd
import os
import akshare as ak
import datetime

import trading.collector.constant as cons
import trading.api.eastmoney as tae
from trading.config.logger import logger


def to_sina_code(code):
    return code[:2] + code[3:]


def from_sina_code(code):
    sl = list(code)
    sl.insert(2, ".")
    return "".join(sl)


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


# 采集A股票基本资料
def save_stock_basic():
    """
    获取A股票基本资料
    返回数据说明
    code	证券代码
    name	证券名称
    """
    result = tae.stock_zh_a_spot_em()
    result = result[result['最新价'].notna()]
    result = result[['代码', '名称']]
    result.sort_values(by='代码', inplace=True)
    # 结果集输出到csv文件
    result.to_csv(cons.stock_basic_file, encoding="utf-8", index=False)
    logger.info('A股票基本资料采集成功.')


# 获取A股历史K线数据(全采集)
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

    # file_name = os.path.join(cons.stock_history_path, code + ".csv")
    # exists = os.path.exists(file_name)
    data = ak.stock_zh_a_hist(code, start_date, end_date, adjust)
    # if (exists):
    #     data = pd.read_csv(file_name)
    #     data.index = pd.DatetimeIndex(data['日期'])
    #     data = data.sort_index()
    #     start_date = data['日期'].values[-1].replace('-', '')
    #     # 去掉最后一行数据
    #     data = data[:-1]
    #     data.reset_index(inplace=True, drop=True)
    # result = ak.stock_zh_a_hist(code, start_date, end_date, adjust)
    # if(data is not None):
    #     data = pd.concat([data, result])
    # else:
    #     data = result
    # 结果集输出到csv文件
    data.to_csv(os.path.join(cons.stock_history_path, code + ".csv"), encoding="utf-8", index=False)


# 每日更新股票数据
def update_k_data_daliy():
    # 判断是否是交易日并且是开盘之后,开盘之前获取的是昨日的数据,会有问题
    today = datetime.datetime.today()
    todayStr = today.strftime('%Y-%m-%d')
    isTradeDay = is_trade_date(todayStr)
    isTradeTime = int(today.strftime('%H%M%S')) - int(datetime.time(9, 30, 0).strftime('%H%M%S')) > 0
    if not (isTradeDay and isTradeTime):
        logger.warning('当日交易未开始,不进行更新')
        return
    df = tae.stock_zh_a_spot_em()
    df = df[df['最新价'].notna()]
    df = df[['代码', '名称', '今开', '最新价', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率', '总市值', '流通市值', '市盈率-动态', '市净率', '量比']]
    df.rename(columns={'今开': '开盘', '最新价': '收盘'}, inplace=True)
    df.insert(1, '日期', today.strftime('%Y-%m-%d'))
    logger.info('更新每日股票数据开始.')
    for index in df.index:
        row = df.loc[index, :]
        code = getattr(row, '代码')
        file_name = os.path.join(cons.stock_history_path, code + ".csv")
        exists = os.path.exists(file_name)
        data = pd.DataFrame(columns=['日期', '代码', '名称', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率', '总市值', '流通市值', '市盈率-动态', '市净率', '量比'])
        if(exists):
            data = pd.read_csv(file_name, dtype={'代码': str})
            data = data[~(data['日期'] == todayStr)]
        data = data.append(row)
        # 结果集输出到csv文件
        data.to_csv(os.path.join(cons.stock_history_path, code + ".csv"), encoding="utf-8", index=False)
        logger.info(code + ':更新成功.')
    logger.info('更新每日股票数据结束.')


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
    logger.info('更新北向资金数据结束.')


# 业绩预告
def save_forecast(date):
    """
    date 注意取值,只能为每季度末日期,例如,2020-03-31,2020-06-30,2020-09-30,2020-12-31
    """
    df = ak.stock_em_yjyg(date)
    df.to_csv(os.path.join(cons.stock_forecast_path, date + cons.file_type_csv), encoding="utf-8", index=False)


if __name__ == '__main__':
    save_stock_basic()
