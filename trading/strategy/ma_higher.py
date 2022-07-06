# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 均线多头策略,选出当前5日,10日,20日线为多头排列,并且多头出现的天数按由少到多排列的股票
卖出策略为,5日均线下穿10日均线警示,5日均线下穿20日均线卖出
"""

import os
import datetime
import pandas as pd

import trading.collector.constant as ccons
import trading.strategy.calc as calc
import trading.strategy.constant as scons
from trading.config.logger import logger


ma_list = [5, 10, 20]
ma_column = ['ma_5', 'ma_10', 'ma_20']


# 个股均线趋势
def select_stock_ma(filterLowerDays=1, filterHigherDays=65535, marketValue=0):
    stocks = pd.DataFrame(columns=['日期', '代码', '名称', '总市值', '流通市值', '起始时间', '持续天数'])
    # 读取所有股票列表
    basic = pd.read_csv(ccons.stock_basic_file, dtype={'代码': str})
    for code in basic['代码']:
        file_name = os.path.join(ccons.stock_history_path, code + ".csv")
        exists = os.path.exists(file_name)
        if not exists:
            continue
        # 判断多头趋势
        kdata = pd.read_csv(file_name)
        kdata.index = pd.DatetimeIndex(kdata['日期'])
        calc.df_ma(kdata, field='收盘', ma_list=ma_list)
        higherDays = 0
        kdata = kdata.sort_index(ascending=False)
        df = kdata[ma_column]
        # 均线相减判断是否多头
        isHigher = True
        higherBegin = None
        df = df.diff(axis=1)
        column = ma_column[1:]
        df = df[column]
        for index in df.index:
            row = df.loc[index]
            for j in range(len(column)):
                if row[j] > 0:
                    isHigher = False
                    break
            if isHigher:
                higherDays = higherDays + 1
                higherBegin = row.name.strftime('%Y-%m-%d')
            else:
                break
        # 如果有多头趋势,加入保存列表
        if higherDays > 0:
            # 计算从多头开始时的股价涨幅跟涨速
            point_end = kdata.iloc[0]
            point_begin = kdata[kdata['日期'] == higherBegin].iloc[0]
            slope = calc.get_slope(point_begin['收盘'], point_end['收盘'], higherDays)
            stock = {
                        '日期': datetime.datetime.today().strftime('%Y-%m-%d'),
                        '代码': code, '名称': kdata.iloc[0]['名称'],
                        '总市值': kdata.iloc[0]['总市值'], '流通市值': kdata.iloc[0]['流通市值'],
                        '起始时间': higherBegin, '持续天数': higherDays, '涨幅(%)': slope['range'], '涨速': slope['speed']
                    }
            stocks = stocks.append(stock, ignore_index=True)
    # 按持续天数排序
    stocks.sort_values(by=['持续天数', '流通市值'], ascending=[0, 0], inplace=True)
    stocks = stocks[(stocks['持续天数'] >= filterLowerDays) & (stocks['持续天数'] <= filterHigherDays)]
    stocks = stocks[stocks['流通市值'] >= marketValue * 100000000]
    stocks.to_csv(scons.ma_higher_stock_file, encoding="utf-8", index=False)
    logger.info('股票均线多头策略,执行完成')


def sell_stock_ma():
    stockdata = pd.read_csv(os.path.join(scons.ma_higher_path, 'stock.csv'), dtype={'代码': str})
    data = stockdata[stockdata['买卖标志'] == 0]
    data.index = pd.DatetimeIndex(data['日期'])
    data.sort_index(inplace=True)
    data.drop_duplicates(subset=['代码'], keep='first', inplace=True)

    sellStocks = pd.DataFrame(columns=['日期', '代码', '名称', '买入日期', '卖出日期', '收盘', '涨幅', '跌幅', '持有天数'])


# 板块指数均线趋势
def select_board_index_ma(board='1', filterLowerDays=1, filterHigherDays=65535):
    """
    :board '1'=行业板块均线趋势,'2'=概念板块均线趋势
    """
    results = pd.DataFrame(columns=['日期', '代码', '名称', '成交量', '成交额', '起始时间', '持续天数'])
    # 获取所有板块指数
    ilist = pd.read_csv(ccons.industry_list_file if board == '1' else ccons.concept_list_file, dtype={'代码': str})
    for code in ilist['代码']:
        # 指数文件不存在,跳过
        filepath = os.path.join(ccons.industry_index_path if board == '1' else ccons.concept_index_path, code + ccons.file_type_csv)
        if not os.path.exists(filepath):
            continue
        # 判断多头趋势
        data = pd.read_csv(filepath, dtype={'代码': str})
        # 不满20天的指数没有均线,跳过
        if data.shape[0] <= 20:
            continue
        data.index = pd.DatetimeIndex(data['日期'])
        calc.df_ma(data, field='收盘价', ma_list=ma_list)
        higherDays = 0
        data = data.sort_index(ascending=False)
        df = data[ma_column]
        # 均线相减判断是否多头
        isHigher = True
        higherBegin = None
        df = df.diff(axis=1)
        column = ma_column[1:]
        df = df[column]
        for index in df.index:
            row = df.loc[index]
            for j in range(len(column)):
                if row[j] > 0:
                    isHigher = False
                    break
            if isHigher:
                higherDays = higherDays + 1
                higherBegin = row.name.strftime('%Y-%m-%d')
            else:
                break
        # 如果有多头趋势,加入保存列表
        if higherDays > 0:
            # 计算从多头开始时的股价涨幅跟涨速
            point_end = data.iloc[0]
            point_begin = data[data['日期'] == higherBegin].iloc[0]
            slope = calc.get_slope(point_begin['收盘价'], point_end['收盘价'], higherDays)
            result = {
                        '日期': datetime.datetime.today().strftime('%Y-%m-%d'),
                        '代码': code, '名称': data.iloc[0]['名称'],
                        '成交量': data.iloc[0]['成交量'], '成交额': data.iloc[0]['成交额'],
                        '起始时间': higherBegin, '持续天数': higherDays, '涨幅(%)': slope['range'], '涨速': slope['speed']
                    }
            results = results.append(result, ignore_index=True)
    # 按持续天数排序
    results.sort_values(by=['持续天数'], ascending=[0], inplace=True)
    results = results[(results['持续天数'] >= filterLowerDays) & (results['持续天数'] <= filterHigherDays)]
    prefix = '行业' if board == '1' else '概念'
    filename = scons.ma_higher_industry_index_file if board == '1' else scons.ma_higher_concept_index_file
    results.to_csv(filename, encoding="utf-8", index=False)
    logger.info(prefix + '指数均线多头策略,执行完成')


if __name__ == '__main__':
    # select_stock_ma()
    # select_board_index_ma('1')
    select_board_index_ma('2')
