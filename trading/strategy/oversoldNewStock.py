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


def selectOversoldStock(publicDays=180, maxDrawdown=60):
    stocks = pd.DataFrame(columns=['日期', '代码', '名称', '最大回撤', '回撤最高日期', '回撤最低日期', '总市值', '流通市值'])
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
                        '总市值': kdata.iloc[-1]['总市值'], '流通市值': kdata.iloc[-1]['流通市值']
                    }
            stocks = stocks.append(stock, ignore_index=True)
    # 按流通市值排序
    stocks.sort_values(by='流通市值', inplace=True)
    path = os.path.join(scons.strategy_path, "over_sold_new_stock")
    if not os.path.exists(path):
        os.mkdir(path)
    stocks.to_csv(os.path.join(path, 'stock' + scons.file_type_csv), mode='a', encoding="utf-8", index=False)
    logger.info('超跌次新股搏反弹策略,执行完成')


if __name__ == '__main__':
    selectOversoldStock()
