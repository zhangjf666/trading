# -*- coding:utf-8 -*-
"""
Date: 2023-09-18 22:00:56
Desc: 均线-布林带买卖回测
"""

import os
import datetime
import pandas as pd

import trading.collector.constant as ccons
import trading.strategy.calc as calc
import trading.strategy.constant as scons
from trading.config.logger import logger

ma_list = [50, 60, 70]
ma_column = ['ma_50', 'ma_60', 'ma_70']
price_column = ['开盘', '收盘', '最高', '最低']


# 个股回测
def backtesting_ma_bolling(code):
    file_name = os.path.join(ccons.stock_history_path, code+".csv")
    exist = os.path.exists(file_name)
    if not exist:
        return
    # 获取均线排列跟布林带数据
    kdata = pd.read_csv(file_name)
    kdata.index = pd.DatetimeIndex(kdata['日期'])
    calc.df_ma(kdata, field='收盘', ma_list=ma_list)
    calc.df_bolling(kdata, field='收盘')
    # 定义需要输出的数据
    # 交易次数
    trade_times = 0
    # 盈利次数
    win_times = 0
    # 亏损次数
    lose_times= 0
    # 总盈利/亏损(使用盈亏比表示)
    profit_ratio = 0
    # 平均交易频率
    average_ransaction_requency = 0
    # 胜率
    win_chance = 0
    # 交易详情列表,包括进场日期,进场方向,进场价格,止损位置,出场日期,出场价格,持有天数,盈亏比
    trading_list = []

    # 判断是否均线多头
    isHigher = False
    isLower = False
    isCrossing = False
    isCrossed = False
    currentPosition = {}
    for index in kdata.index:
        row = kdata.loc[index]
        # 当前是否有持仓,有持仓判断出场,无持仓判断入场
        if currentPosition['holding'] is True:
            continue
        else:
            # 判断是否满足入场条件
            # 1.均线多头或者空头排列
            ma1 = row[ma_column[0]]
            ma2 = row[ma_column[1]]
            ma3 = row[ma_column[2]]
            if(ma1 < ma2 < ma3):
                isLower = True
            if(ma1 > ma2 > ma3):
                isHigher = True
            # 2.如果之前没有出现穿越布林带,判断是否穿过了布林带的上轨跟下轨(多头下轨,空头上轨)
            if isCrossed is False:
                # 穿过布林带,可能为入场位,记录下止损价
                if isLower:
                    # 判断上穿布林带
                    if row['upper_bound'].betweent(row['最低'], row['最高'], inclusive='right'):
                        isCrossing = True
                        currentPosition['stop'] = row['最高']
                        isCrossed = True
                if isHigher:
                    # 判断下穿布林带
                    if row['lower_bound'].betweent(row['最高'], row['最低'], inclusive='right'):
                        isCrossing = True
                        currentPosition['stop'] = row['最低']
                        isCrossed = True
            # 3.如果已经出现穿越,则看当前是否是收出了阳线(做多)或者阴线(做空),符合条件就进场
            # 进场条件为多头排列时,价格下穿布林带下轨后收出回到布林带中第一个阳线,空头排列时,价格上
            # 穿布林带上轨后收出回到布林带中第一个阴线
            else:


        