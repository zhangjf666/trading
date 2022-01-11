# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 股票数据获取
"""

from logging import log
import traceback
import pandas as pd
import os
import akshare as ak
import datetime
import trading.collector.constant as cons
import trading.api.eastmoney as em
import trading.api.ths as ths
import trading.api.sina as sina
import trading.api.common as api
from trading.config.logger import logger
import trading.util.common_util as util


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
    logger.info('交易日历更新成功.')


# 获取某个日期的后一个交易日, offset 偏移量,正值向后,负值向前
def next_trade_date(date, offset: int = 1):
    tf = pd.read_csv(cons.stock_tradedate_file)
    tf['trade_date'] = pd.to_datetime(tf['trade_date'])
    tf.sort_values('trade_date')
    tf = tf[tf['trade_date'] >= date] if offset >= 0 else tf[tf['trade_date'] < date]
    return pd.Timestamp(tf['trade_date'].values[offset]).to_pydatetime().strftime('%Y-%m-%d')


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
    result = em.stock_zh_a_spot_em()
    result = result[result['最新价'].notna()]
    result = result[['代码', '名称']]
    result.sort_values(by='代码', inplace=True)
    # 结果集输出到csv文件
    result.to_csv(cons.stock_basic_file, encoding="utf-8", index=False)
    logger.info('A股票基本资料采集成功.')


# 获取A股历史K线数据(全采集)
def save_history_k_data(code,
                        name,
                        start_date='19800101',
                        end_date='21211231',
                        adjust=""):
    """
    获取A股历史K线数据
    入参
    code:股票代码，6位数字代码，此参数不可为空；
    start_date:开始日期（包含），格式“YYYYMMDD”，为空时取19900101；
    end_date:结束日期（包含），格式“YYYYMMDD”，为空时取最近一个交易日；
    adjust:复权类型，默认不复权,qfq:前复权,hfq:后复权
    """

    # file_name = os.path.join(cons.stock_history_path, code + ".csv")
    # exists = os.path.exists(file_name)
    data = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, adjust=adjust)
    data.insert(1, '代码', code)
    data.insert(2, '名称', name)
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


# 更新股票历史数据
def update_history_k_data(code, name='', start_date='19800101', end_date='21211231', adjust=""):
    """
    获取A股历史K线数据
    入参
    code:股票代码，6位数字代码，此参数不可为空；
    start_date:开始日期（包含），格式“YYYYMMDD”，为空时取19900101；
    end_date:结束日期（包含），格式“YYYYMMDD”，为空时取最近一个交易日；
    adjust:复权类型，默认不复权,qfq:前复权,hfq:后复权
    """

    file_name = os.path.join(cons.stock_history_path, code + ".csv")
    exists = os.path.exists(file_name)
    if (exists):
        data = pd.read_csv(file_name, dtype={'代码': str})
        data.index = pd.DatetimeIndex(data['日期'])
        data = data.sort_index()
        # 分割更新日期前后的数据
        start_time = datetime.datetime.strptime(start_date, '%Y%m%d')
        front_data = data[data.index < start_time]
        front_data.reset_index(inplace=True, drop=True)
        end_time = datetime.datetime.strptime(end_date, '%Y%m%d')
        after_data = data[data.index > end_time]
        after_data.reset_index(inplace=True, drop=True)
        result = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, adjust=adjust)
        result.insert(1, '代码', code)
        result.insert(2, '名称', name)
        alldata = pd.concat([front_data, result])
        alldata = pd.concat([alldata, after_data])
        # 结果集输出到csv文件
        alldata.to_csv(os.path.join(cons.stock_history_path, code + ".csv"), encoding="utf-8", index=False)


# 每日更新股票数据
def update_k_data_daliy():
    # 判断是否是交易日并且是开盘之后,开盘之前获取的是昨日的数据,会有问题
    today = datetime.datetime.today()
    dateStr = today.strftime('%Y-%m-%d')
    isTradeDay = is_trade_date(dateStr)
    isTradeTime = int(today.strftime('%H%M%S')) - int(datetime.time(9, 30, 0).strftime('%H%M%S')) > 0
    if not isTradeDay or not isTradeTime:
        dateStr = next_trade_date(dateStr, offset=-1)
    df = em.stock_zh_a_spot_em()
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
            data = data[~(data['日期'] == dateStr)]
        data = data.append(row)
        data.sort_values(by='日期', inplace=True)
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


# 更新概念板块列表
def update_concept_board():
    """
    更新概念板块列表
    """
    df = ths.stock_board_concept_name_ths()
    df.rename(columns={'代码': 'url', '概念名称': '名称'}, inplace=True)
    df['代码'] = df['url'].map(lambda x: x.replace('http://q.10jqka.com.cn/gn/detail/code/', '')[0:-1])
    df.drop_duplicates(inplace=True)
    df.to_csv(cons.concept_list_file, encoding="utf-8", index=False)
    logger.info('更新概念板块列表结束')


# 更新概念板块成分股
def update_concept_stocks():
    """
    更新概念板块成分股
    """
    if not os.path.exists(cons.concept_list_file):
        logger.info('需先更新概念板块列表')
        return
    concept_list = pd.read_csv(cons.concept_list_file, dtype={'代码': str})
    if(os.path.exists(cons.concept_stocks_file)):
        stocks = pd.read_csv(cons.concept_stocks_file)
    else:
        stocks = pd.DataFrame()
    for index in concept_list.index:
        row = concept_list.loc[index, :]
        code = row['代码']
        name = row['名称']
        temp = ths.stock_board_concept_cons_ths(code)
        temp.drop(['序号'], axis=1, inplace=True)
        temp['概念代码'] = code
        temp['概念名称'] = name
        if stocks.empty:
            stocks = temp
        else:
            stocks = stocks[~(stocks['概念代码'] == int(code))]
            stocks = stocks.append(temp)
        stocks.to_csv(cons.concept_stocks_file, encoding="utf-8", index=False)
        logger.info('[' + code + ']' + name + ' 更新成功')
    logger.info('更新概念板块成分股结束')


# 更新概念板块指数
def update_concept_index(code: str = None, name: str = None, start_year: str = None, end_year: str = None):
    """
    更新概念板块指数
    """
    if not start_year:
        start_year = datetime.datetime.now().year
    if not end_year:
        end_year = datetime.datetime.now().year
    temp = ths.stock_board_concept_index_ths(code, start_year, end_year)
    if temp.empty:
        return
    temp['代码'] = code
    temp['名称'] = name
    # 数据整合进文件
    filename = os.path.join(cons.concept_index_path, code + cons.file_type_csv)
    if not os.path.exists(filename):
        alldata = temp
    else:
        data = pd.read_csv(filename, dtype={'代码': str})
        data.index = pd.DatetimeIndex(data['日期'])
        data.sort_index()
        start_time = datetime.date(int(start_year), 1, 1)
        front_data = data[data.index < pd.Timestamp(start_time)]
        front_data.reset_index(inplace=True, drop=True)
        end_time = datetime.date(int(end_year), 12, 31)
        after_data = data[data.index > pd.Timestamp(end_time)]
        after_data.reset_index(inplace=True, drop=True)
        alldata = pd.concat([front_data, temp])
        alldata = pd.concat([alldata, after_data])
    alldata.to_csv(filename, encoding="utf-8", index=False)
    logger.info('[' + code + ']' + name + ' 更新成功')


# 更新所有概念板块指数
def update_all_concept_index(start_year: str = None, end_year: str = None):
    """
    更新所有概念板块指数
    """
    if not os.path.exists(cons.concept_list_file):
        logger.info('需先更新概念板块列表')
        return
    if not start_year:
        start_year = datetime.datetime.now().year
    if not end_year:
        end_year = datetime.datetime.now().year
    concept_list = pd.read_csv(cons.concept_list_file, dtype={'代码': str})
    for index in concept_list.index:
        row = concept_list.loc[index, :]
        code = row['代码']
        name = row['名称']
        update_concept_index(code, name, start_year, end_year)
    logger.info('更新概念板块指数结束')


# 更新行业板块列表
def update_industry_board():
    """
    更新行业板块列表
    """
    df = ths.stock_board_industry_name_ths()
    df.drop_duplicates()
    df.to_csv(cons.industry_list_file, encoding="utf-8", index=False)
    logger.info('更新行业板块列表结束')


# 更新行业板块成分股
def update_industry_stocks():
    """
    更新行业板块成分股
    """
    if not os.path.exists(cons.industry_list_file):
        logger.info('需先更新行业板块列表')
        return
    industry_list = pd.read_csv(cons.industry_list_file, dtype={'代码': str})
    if(os.path.exists(cons.industry_stocks_file)):
        stocks = pd.read_csv(cons.industry_stocks_file)
    else:
        stocks = pd.DataFrame()
    for index in industry_list.index:
        row = industry_list.loc[index, :]
        code = row['代码']
        name = row['名称']
        temp = ths.stock_board_cons_ths(code)
        temp.drop(['序号'], axis=1, inplace=True)
        temp['行业代码'] = code
        temp['行业名称'] = name
        if stocks.empty:
            stocks = temp
        else:
            stocks = stocks[~(stocks['行业代码'] == int(code))]
            stocks = stocks.append(temp)
        stocks.to_csv(cons.industry_stocks_file, encoding="utf-8", index=False)
        logger.info('[' + code + ']' + name + ' 更新成功')
    logger.info('更新行业板块成分股结束')


# 更新行业板块指数
def update_industry_index(code: str = None, name: str = None, start_year: str = None, end_year: str = None):
    """
    更新行业板块指数
    """
    if not start_year:
        start_year = datetime.datetime.now().year
    if not end_year:
        end_year = datetime.datetime.now().year
    temp = ths.stock_board_industry_index_ths(code, start_year, end_year)
    temp['代码'] = code
    temp['名称'] = name
    # 数据整合进文件
    filename = os.path.join(cons.industry_index_path, code + cons.file_type_csv)
    if not os.path.exists(filename):
        alldata = temp
    else:
        data = pd.read_csv(filename, dtype={'代码': str})
        data.index = pd.DatetimeIndex(data['日期'])
        data.sort_index()
        start_time = datetime.date(int(start_year), 1, 1)
        front_data = data[data.index < pd.Timestamp(start_time)]
        front_data.reset_index(inplace=True, drop=True)
        end_time = datetime.date(int(end_year), 12, 31)
        after_data = data[data.index > pd.Timestamp(end_time)]
        after_data.reset_index(inplace=True, drop=True)
        alldata = pd.concat([front_data, temp])
        alldata = pd.concat([alldata, after_data])
    alldata.to_csv(filename, encoding="utf-8", index=False)
    logger.info('[' + code + ']' + name + ' 更新成功')


# 更新所有行业板块指数
def update_all_industry_index(start_year: str = None, end_year: str = None):
    """
    更新所有行业板块指数
    """
    if not os.path.exists(cons.industry_list_file):
        logger.info('需先更新行业板块列表')
        return
    if not start_year:
        start_year = datetime.datetime.now().year
    if not end_year:
        end_year = datetime.datetime.now().year
    industry_list = pd.read_csv(cons.industry_list_file, dtype={'代码': str})
    for index in industry_list.index:
        row = industry_list.loc[index, :]
        code = row['代码']
        name = row['名称']
        update_industry_index(code, name, start_year, end_year)
    logger.info('更新行业板块指数结束')


# 可转债比价表
def update_convertible():
    """
    更新可转债比价表
    """
    df = em.bond_cov_comparison()
    df = df[~(df['转债最新价'] == '-')]
    df['双低值'] = df['转债最新价'] + df['转股溢价率'] * 100
    df.sort_values(by='双低值', inplace=True)
    df['双低值'] = df['双低值'].apply(lambda x: format(x, '.2f'))
    df.insert(0, '日期', datetime.datetime.today().strftime('%Y-%m-%d'))
    df.drop(columns=['序号'], inplace=True)
    df.to_csv(cons.convertible_file, encoding='utf-8', index=False)
    logger.info('可转债比价表更新结束')


# 保存指数列表
def update_index():
    """
    更新指数列表
    """
    df = sina.stock_zh_index_spot()
    df = df[~(df['名称'] == '')]
    df = df[['代码', '名称']]
    df.rename(columns={'代码': 'sina_code'}, inplace=True)
    df['代码'] = df['sina_code'].map(lambda x: x[2:])
    df.to_csv(cons.index_list_file, encoding='utf-8', index=False)
    logger.info('指数列表更新结束')


# 每日更新指数数据
def update_index_daily():
    """
    每日更新指数数据
    """
    today = datetime.datetime.today()
    dateStr = today.strftime('%Y-%m-%d')
    isTradeDay = is_trade_date(dateStr)
    isTradeTime = int(today.strftime('%H%M%S')) - int(datetime.time(9, 30, 0).strftime('%H%M%S')) > 0
    if not isTradeDay or not isTradeTime:
        dateStr = next_trade_date(dateStr, offset=-1)
    df = sina.stock_zh_index_spot()
    df = df[~(df['名称'] == '')]
    df['代码'] = df['代码'].map(lambda x: x[2:])
    df = df[['代码', '名称', '今开', '最新价', '最高', '最低', '成交量', '成交额']]
    df.rename(columns={'今开': '开盘', '最新价': '收盘'}, inplace=True)
    df.insert(1, '日期', dateStr)
    logger.info('更新每日指数数据开始.')
    for index in df.index:
        row = df.loc[index, :]
        code = getattr(row, '代码')
        name = getattr(row, '名称')
        file_name = os.path.join(cons.index_history_path, code + ".csv")
        exists = os.path.exists(file_name)
        data = pd.DataFrame(columns=['日期', '代码', '名称', '开盘', '收盘', '最高', '最低', '成交量', '成交额'])
        if(exists):
            data = pd.read_csv(file_name, dtype={'代码': str})
            data = data[~(data['日期'] == dateStr)]
        data = data.append(row)
        data.sort_values(by='日期', inplace=True)
        # 结果集输出到csv文件
        data.to_csv(os.path.join(cons.index_history_path, code + ".csv"), encoding="utf-8", index=False)
        logger.info('[' + code + ']' + name + ':更新成功.')
    logger.info('更新每日指数数据结束.')


# 保存指数历史日频数据
def update_index_history():
    """
    保存指数历史日频数据
    """
    basic = pd.read_csv(cons.index_list_file, dtype={'代码': str})
    for index in basic.index:
        row = basic.loc[index, :]
        scode = row['sina_code']
        code = row['代码']
        name = row['名称']
        try:
            data = sina.stock_zh_index_daily(symbol=scode)
            data.rename(columns={'date': '日期', 'open': '开盘', 'close': '收盘', 'high': '最高', 'low': '最低', 'volume': '成交量'}, inplace=True)
            data.insert(1, '代码', code)
            data.insert(2, '名称', name)
            data.to_csv(os.path.join(cons.index_history_path, code + ".csv"), encoding="utf-8", index=False)
            logger.info('[' + code + ']' + name + ' 采集成功')
            util.sleep()
        except BaseException:
            logger.error('[' + code + ']' + name + ' 采集失败,原因:' + traceback.format_exc())
    logger.info('指数日频数据更新成功')


# 更新指数成分股
def update_index_stocks():
    """
    更新指数成分股
    """
    if not os.path.exists(cons.index_list_file):
        logger.info('需先更新指数列表')
        return
    index_list = pd.read_csv(cons.index_list_file, dtype={'代码': str})
    if(os.path.exists(cons.index_stocks_file)):
        stocks = pd.read_csv(cons.index_stocks_file)
    else:
        stocks = pd.DataFrame()
    for index in index_list.index:
        try:
            row = index_list.loc[index, :]
            code = row['代码']
            name = row['名称']
            temp = api.index_stock_cons_csindex(code)
            temp['指数代码'] = code
            temp['指数名称'] = name
            if stocks.empty:
                stocks = temp
            else:
                stocks = stocks[~(stocks['指数代码'] == int(code))]
                stocks = stocks.append(temp)
            stocks.to_csv(cons.index_stocks_file, encoding="utf-8", index=False)
            logger.info('[' + code + ']' + name + ' 更新成功')
            util.sleep()
        except BaseException:
            logger.error('[' + code + ']' + name + ' 采集失败,原因:' + traceback.format_exc())
    logger.info('更新指数成分股结束')


# 机构调研统计
def update_jgdy_tj():
    """
    更新机构调研统计
    """
    start_date = '2022-01-01'
    df = pd.DataFrame()
    if os.path.exists(cons.jgdytj_file):
        df = pd.read_csv(cons.jgdytj_file, dtype={'代码': str})
        df.sort_values(by='接待日期', inplace=True)
        start_date = df['接待日期'].values[-1]
    logger.info('更新机构调研统计开始.更新时间: ' + start_date)
    try:
        temp = em.stock_em_jgdy_tj(start_date)
        temp = temp[["代码", "名称",  "接待机构数量", "接待方式", "接待人员", "接待地点", "接待日期", "公告日期"]]
        df = df.append(temp)
        df.to_csv(cons.jgdytj_file, encoding="utf-8", index=False)
        logger.info('更新机构调研统计结束')
    except BaseException:
        logger.error('更新机构调研统计出错:' + traceback.format_exc())


# 每日更新创新高技术指标
def update_cxg_daily():
    """
    创新高技术指标
    """
    try:
        logger.info('更新创新高技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_cxg_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        if os.path.exists(cons.cxg_file):
            df.to_csv(cons.cxg_file, mode='a', header=False, encoding="utf-8", index=False)
        else:
            df.to_csv(cons.cxg_file, encoding="utf-8", index=False)
        logger.info('更新创新高技术指标结束.')
    except BaseException:
        logger.error('更新创新高技术指标出错:' + traceback.format_exc())


# 每日更新创新低技术指标
def update_cxd_daily():
    """
    创新低技术指标
    """
    try:
        logger.info('更新创新低技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_cxd_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        if os.path.exists(cons.cxd_file):
            df.to_csv(cons.cxd_file, mode='a', header=False, encoding="utf-8", index=False)
        else:
            df.to_csv(cons.cxd_file, encoding="utf-8", index=False)
        logger.info('更新创新低技术指标结束.')
    except BaseException:
        logger.error('更新创新低技术指标出错:' + traceback.format_exc())


# 每日更新连续上涨技术指标
def update_lxsz_daily():
    """
    连续上涨技术指标
    """
    try:
        logger.info('更新连续上涨技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_lxsz_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(cons.lxsz_file, encoding="utf-8", index=False)
        logger.info('更新连续上涨技术指标结束.')
    except BaseException:
        logger.error('更新连续上涨技术指标出错:' + traceback.format_exc())


# 每日更新连续下跌技术指标
def update_lxxd_daily():
    """
    连续下跌技术指标
    """
    try:
        logger.info('更新连续下跌技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_lxxd_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(cons.lxxd_file, encoding="utf-8", index=False)
        logger.info('更新连续下跌技术指标结束.')
    except BaseException:
        logger.error('更新连续下跌技术指标出错:' + traceback.format_exc())


# 每日更新持续放量技术指标
def update_cxfl_daily():
    """
    持续放量技术指标
    """
    try:
        logger.info('更新持续放量技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_cxfl_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(cons.cxfl_file, encoding="utf-8", index=False)
        logger.info('更新持续放量技术指标结束.')
    except BaseException:
        logger.error('更新持续放量技术指标出错:' + traceback.format_exc())


# 每日更新持续缩量技术指标
def update_cxsl_daily():
    """
    持续缩量技术指标
    """
    try:
        logger.info('更新持续缩量技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_cxsl_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(cons.cxsl_file, encoding="utf-8", index=False)
        logger.info('更新持续缩量技术指标结束.')
    except BaseException:
        logger.error('更新持续缩量技术指标出错:' + traceback.format_exc())


# 每日更新量价齐升技术指标
def update_ljqs_daily():
    """
    量价齐升技术指标
    """
    try:
        logger.info('更新量价齐升技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_ljqs_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(cons.ljqs_file, encoding="utf-8", index=False)
        logger.info('更新量价齐升技术指标结束.')
    except BaseException:
        logger.error('更新量价齐升技术指标出错:' + traceback.format_exc())


# 每日更新量价齐跌技术指标
def update_ljqd_daily():
    """
    量价齐跌技术指标
    """
    try:
        logger.info('更新量价齐跌技术指标开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_rank_ljqd_ths()
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(cons.ljqd_file, encoding="utf-8", index=False)
        logger.info('更新量价齐跌技术指标结束.')
    except BaseException:
        logger.error('更新量价齐跌技术指标出错:' + traceback.format_exc())


# 每日个股资金排行
def update_ggzj_daily(symbol: str = "5日排行"):
    """
    个股资金排行
    :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
    """
    try:
        logger.info('更新个股资金' + symbol + '排行开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_fund_flow_individual(symbol)
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(os.path.join(cons.zjlx_path, 'ggzj-' + symbol + cons.file_type_csv), encoding="utf-8", index=False)
        logger.info('更新个股资金' + symbol + '排行结束.')
    except BaseException:
        logger.error('更新个股资金' + symbol + '排行出错:' + traceback.format_exc())


# 每日概念资金排行
def update_gnzj_daily(symbol: str = "5日排行"):
    """
    概念资金排行
    :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
    """
    try:
        logger.info('更新概念资金' + symbol + '排行开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_fund_flow_concept(symbol)
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(os.path.join(cons.zjlx_path, 'gnzj-' + symbol + cons.file_type_csv), encoding="utf-8", index=False)
        logger.info('更新概念资金' + symbol + '排行结束.')
    except BaseException:
        logger.error('更新概念资金' + symbol + '排行出错:' + traceback.format_exc())


# 每日行业资金排行
def update_hyzj_daily(symbol: str = "5日排行"):
    """
    行业资金排行
    :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
    """
    try:
        logger.info('更新行业资金' + symbol + '排行开始.')
        dateStr = datetime.datetime.today().strftime('%Y-%m-%d')
        df = ths.stock_fund_flow_industry(symbol)
        df.drop(columns=['序号'], inplace=True)
        df.rename(columns={'股票代码': '代码', '股票简称': '名称'}, inplace=True)
        df.insert(0, '日期', dateStr)
        df.to_csv(os.path.join(cons.zjlx_path, 'hyzj-' + symbol + cons.file_type_csv), encoding="utf-8", index=False)
        logger.info('更新行业资金' + symbol + '排行结束.')
    except BaseException:
        logger.error('更新行业资金' + symbol + '排行出错:' + traceback.format_exc())


if __name__ == '__main__':
    update_jgdy_tj()
    update_cxg_daily()
    update_cxd_daily()
    update_lxsz_daily()
    update_lxxd_daily()
    update_cxfl_daily()
    update_cxsl_daily()
    update_ljqs_daily()
    update_ljqd_daily()
    update_ggzj_daily(symbol='3日排行')
    update_ggzj_daily(symbol='5日排行')
    update_ggzj_daily(symbol='10日排行')
    update_ggzj_daily(symbol='20日排行')
    update_gnzj_daily(symbol='3日排行')
    update_gnzj_daily(symbol='5日排行')
    update_gnzj_daily(symbol='10日排行')
    update_gnzj_daily(symbol='20日排行')
    update_hyzj_daily(symbol='3日排行')
    update_hyzj_daily(symbol='5日排行')
    update_hyzj_daily(symbol='10日排行')
    update_hyzj_daily(symbol='20日排行')
