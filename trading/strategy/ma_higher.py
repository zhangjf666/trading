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


def select_ma_higher(filterHigherDays=20, marketValue=100):
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
            stock = {
                        '日期': datetime.datetime.today().strftime('%Y-%m-%d'),
                        '代码': code, '名称': kdata.iloc[0]['名称'],
                        '总市值': kdata.iloc[0]['总市值'], '流通市值': kdata.iloc[0]['流通市值'],
                        '起始时间': higherBegin, '持续天数': higherDays
                    }
            stocks = stocks.append(stock, ignore_index=True)
    # 按持续天数排序
    stocks.sort_values(by=['持续天数', '流通市值'], ascending=[0, 0], inplace=True)
    stocks = stocks[stocks['持续天数'] >= filterHigherDays]
    stocks = stocks[stocks['流通市值'] >= marketValue * 100000000]
    path = os.path.join(scons.strategy_path, "ma_higher")
    if not os.path.exists(path):
        os.mkdir(path)
    filename = os.path.join(path, 'stock' + scons.file_type_csv)
    stocks.to_csv(filename, mode='a', encoding="utf-8", index=False, header=None if os.path.isfile(filename) else True)
    logger.info('均线多头策略,执行完成')


def sell_ma_higher():
    stockdata = pd.read_csv(os.path.join(scons.ma_higher_path, 'stock.csv'), dtype={'代码': str})
    data = stockdata[stockdata['买卖标志'] == 0]
    data.index = pd.DatetimeIndex(data['日期'])
    data.sort_index(inplace=True)
    data.drop_duplicates(subset=['代码'], keep='first', inplace=True)

    sellStocks = pd.DataFrame(columns=['日期', '代码', '名称', '买入日期', '卖出日期', '收盘', '涨幅', '跌幅', '持有天数'])

if __name__ == '__main__':
    select_ma_higher()
