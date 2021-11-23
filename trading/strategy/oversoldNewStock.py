# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 超跌次新股搏反弹策略,选出上市小于180个交易日,回撤超过60%的次新股,按流通市值从小到大排列,博大幅反弹,卖出策略为连续5个交易日内涨幅超过20%或者4个交易日下跌超过10%
"""

import os
import datetime
import pandas as pd

import trading.collector.constant as ccons
import trading.strategy.calc as calc
import trading.strategy.constant as scons
from trading.config.logger import logger
import trading.util.file_util as fileUtil


def selectOversoldStock(publicDays=180, maxDrawdown=60):
    stocks = pd.DataFrame(columns=['日期', '代码', '名称', '最大回撤', '回撤最高日期', '回撤最低日期', '总市值', '流通市值', '买卖标志'])
    # 读取所有股票列表
    basic = pd.read_csv(ccons.stock_basic_file, dtype={'代码': str})
    for code in basic['代码']:
        file_name = os.path.join(ccons.stock_history_path, code + ".csv")
        exists = os.path.exists(file_name)
        if not exists:
            continue
        # 判断上市天数
        kdata = pd.read_csv(file_name)
        kdata.index = pd.DatetimeIndex(kdata['日期'])
        startDate = kdata.index[0]
        endDate = kdata.index[-1]
        if (endDate-startDate).days > publicDays:
            continue
        # 计算最大回撤
        drawdown = calc.calc_max_drawdown_detail(kdata, field='收盘')
        if(drawdown['max_drawdown'] >= maxDrawdown):
            stock = {
                        '日期': datetime.datetime.today().strftime('%Y-%m-%d'),
                        '代码': code, '名称': kdata.iloc[-1]['名称'], '最大回撤': drawdown['max_drawdown'],
                        '回撤最高日期': drawdown['max_date'], '回撤最低日期': drawdown['min_date'],
                        '总市值': kdata.iloc[-1]['总市值'], '流通市值': kdata.iloc[-1]['流通市值'], '买卖标志': 0
                    }
            stocks = stocks.append(stock, ignore_index=True)
    # 按流通市值排序
    stocks.sort_values(by='流通市值', inplace=True)
    path = os.path.join(scons.strategy_path, "over_sold_new_stock")
    fileUtil.createPath(path)
    filename = os.path.join(path, 'stock' + scons.file_type_csv)
    stocks.to_csv(filename, mode='a', encoding="utf-8", index=False, header=None if os.path.isfile(filename) else True)
    logger.info('超跌次新股搏反弹策略,执行完成')


def sellOverStock():
    stockdata = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'stock.csv'), dtype={'代码': str})
    data = stockdata[stockdata['买卖标志'] == 0]
    data.index = pd.DatetimeIndex(data['日期'])
    data.sort_index(inplace=True)
    data.drop_duplicates(subset=['代码'], keep='first', inplace=True)

    sellStocks = pd.DataFrame(columns=['日期', '代码', '名称', '买入日期', '卖出日期', '收盘', '涨幅', '跌幅', '持有天数'])
    for i in range(data.index.size):
        row = data.iloc[i]
        code = row['代码']
        date = row['回撤最低日期']
        stock = pd.read_csv(os.path.join(ccons.stock_history_path, code+ccons.file_type_csv), dtype={'代码': str})
        stock.index = pd.DatetimeIndex(stock['日期'])
        stock.sort_index(inplace=True)
        stock = stock[stock.index > date]
        if len(stock.index) == 0:
            continue
        openPrice = stock.iloc[0]['开盘']
        stock['涨'] = stock['收盘'].shift(5)
        stock['跌'] = stock['收盘'].shift(4)
        # 不足5日的nan数据填充为开盘价
        stock.loc[stock['涨'].isna(), '涨'] = openPrice
        stock.loc[stock['跌'].isna(), '跌'] = openPrice
        stock['涨幅'] = stock['收盘'] / stock['涨'] - 1
        stock['跌幅'] = 1 - stock['收盘'] / stock['跌']
        # 卖出条件,涨幅大于0.2, 跌幅大于0.1
        operstock = stock[(stock['涨幅'] > 0.2) | (stock['跌幅'] > 0.1)]
        if operstock.index.size > 0:
            operrow = operstock.iloc[0]
            sellStock = {
                '日期': datetime.datetime.today().strftime('%Y-%m-%d'),
                '代码': code, '名称': row['名称'], '买入日期': date,
                '卖出日期': operrow['日期'], '收盘': operrow['收盘'],
                '涨幅': operrow['涨幅'], '跌幅': operrow['跌幅'],
                '持有天数': (datetime.datetime.strptime(operrow['日期'], '%Y-%m-%d') - datetime.datetime.strptime(date, '%Y-%m-%d')).days
            }
            sellStocks = sellStocks.append(sellStock, ignore_index=True)
            stockdata.loc[stockdata['代码'] == code, '买卖标志'] = 1
    # 更新sell_stock文件
    filename = os.path.join(scons.over_sold_new_stock_path, 'sell_stock' + scons.file_type_csv)
    sellStocks.to_csv(filename, mode='a', encoding="utf-8", index=False, header=None if os.path.isfile(filename) else True)
    # 更新stock文件
    stockdata.to_csv(os.path.join(scons.over_sold_new_stock_path, 'stock.csv'), encoding="utf-8", index=False)
    logger.info('超跌次新股搏反弹策略卖出任务,执行完成')


if __name__ == '__main__':
    selectOversoldStock()
    sellOverStock()
