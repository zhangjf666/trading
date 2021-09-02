# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 超跌次新股搏反弹策略
"""

import os
import pandas as pd

import trading.collector.constant as cons
import trading.strategy.calc as calc


def selectOversoldStock(publicDays=180, maxDrawdown=60):
    stocks = pd.DataFrame(columns=['日期', '代码', '名称', '最大回撤'])
    # 读取所有股票列表
    basic = pd.read_csv(cons.stock_basic_file, dtype={'code': str})
    for code in basic['code']:
        # 判断上市天数
        kdata = pd.read_csv(os.path.join(cons.stock_history_path, code + '.csv'))
        kdata.index = pd.DatetimeIndex(kdata['日期'])
        startDate = kdata.index[0]
        endDate = kdata.index[-1]
        if (endDate-startDate).days < publicDays:
            continue
        # 计算最大回撤
        drawdown = calc.calc_max_drawdown_detail(kdata, field='收盘')
        print(drawdown)
        # if(drawdown >= maxDrawdown):


if __name__ == '__main__':
    selectOversoldStock()
