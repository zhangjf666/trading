# -*- coding:utf-8 -*-
"""
Date: 2023-09-18 22:00:56
Desc: 均线-布林带买卖回测
"""

import os
import traceback
import pandas as pd
from datetime import datetime
import trading.collector.constant as ccons
import trading.strategy.calc as calc
import trading.strategy.constant as scons
from trading.config.logger import logger

ma_list = [50, 60, 70]
ma_column = ['ma_50', 'ma_60', 'ma_70']

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)


# 个股回测
def backtesting_ma_bolling(code, name='', beginTime=None, endTime=None, tradeDirection=0):
    """
    根据均线排列和布林带回测策略
    入参
    code:股票代码，6位数字代码，此参数不可为空;
    name:股票名称
    beginTime:开始日期（包含），格式“%Y-%m-%d”；
    endTime:结束日期（包含），格式“%Y-%m-%d”；
    tradeDirection:交易方向,0:双向,1:只做多,2:只做空
    """
    logger.info('[' + code + ']' + name + '回测开始')
    file_name = os.path.join(ccons.stock_history_path, code+".csv")
    exist = os.path.exists(file_name)
    if not exist:
        logger.info(file_name + '数据文件不存在.回测结束')
        return
    # 获取均线排列跟布林带数据
    kdata = pd.read_csv(file_name)
    kdata.index = pd.DatetimeIndex(kdata['日期'])
    calc.df_ma(kdata, field='收盘', ma_list=ma_list)
    calc.df_bolling(kdata, field='收盘')
    # 筛选时间范围
    if beginTime is not None:
        beginT = datetime.strptime(beginTime, "%Y-%m-%d")
        kdata = kdata[kdata.index >= pd.Timestamp(beginT)]
    if endTime is not None:
        endT = datetime.strptime(endTime, "%Y-%m-%d")
        kdata = kdata[kdata.index <= pd.Timestamp(endT)]
    # 交易详情列表,包括进场日期,进场方向,进场价格,止损位置,出场日期,出场价格,持有天数,盈亏比
    trading_list = []

    # 判断是否均线多头
    isHigher = False
    isLower = False
    # 正在布林带上
    isCrossing = False
    # 是否发生了穿过布林带
    isCrossed = False
    currentPosition = {'holding': False}
    for index in kdata.index:
        row = kdata.loc[index]
        # 当前是否有持仓,有持仓判断出场,无持仓判断入场
        if currentPosition['holding'] is True:
            # 判断出场条件, 做多判断触碰布林上轨,做空判断触碰布林下轨
            if currentPosition['direction'] == 'buy':
                # 触碰上轨,以上轨价格平仓
                if row['最低'] <= row['higher_bound'] <= row['最高']:
                    currentPosition['outDate'] = row['日期']
                    currentPosition['outPrice'] = row['higher_bound']
                    currentPosition['holdDays'] = (datetime.strptime(row['日期'], "%Y-%m-%d") - datetime.strptime(currentPosition['entryDate'], "%Y-%m-%d")).days
                    profitRatio = (currentPosition['outPrice'] - currentPosition['entryPrice']) / (currentPosition['entryPrice'] - currentPosition['stop'])
                    currentPosition['profitRatio'] = profitRatio
                    currentPosition['isWin'] = True
                    isCrossing = False
                    isCrossed = False
                    isHigher = False
                    isLower = False
                    trading_list.append(currentPosition)
                    currentPosition = {'holding': False}
                # 止损
                elif row['最低'] < currentPosition['stop']:
                    currentPosition['outDate'] = row['日期']
                    currentPosition['outPrice'] = currentPosition['stop']
                    currentPosition['holdDays'] = (datetime.strptime(row['日期'], "%Y-%m-%d") - datetime.strptime(currentPosition['entryDate'], "%Y-%m-%d")).days
                    currentPosition['profitRatio'] = -1
                    currentPosition['isWin'] = False
                    isCrossing = False
                    isCrossed = False
                    isHigher = False
                    isLower = False
                    trading_list.append(currentPosition)
                    currentPosition = {'holding': False}
            elif currentPosition['direction'] == 'sell':
                # 触碰下轨,以下轨价格平仓
                if row['最低'] <= row['lower_bound'] <= row['最高']:
                    currentPosition['outDate'] = row['日期']
                    currentPosition['outPrice'] = row['lower_bound']
                    currentPosition['holdDays'] = (datetime.strptime(row['日期'], "%Y-%m-%d") - datetime.strptime(currentPosition['entryDate'], "%Y-%m-%d")).days
                    profitRatio = (currentPosition['entryPrice'] - currentPosition['outPrice']) / (currentPosition['stop'] - currentPosition['entryPrice'])
                    currentPosition['profitRatio'] = profitRatio
                    currentPosition['isWin'] = True
                    isCrossing = False
                    isCrossed = False
                    isHigher = False
                    isLower = False
                    trading_list.append(currentPosition)
                    currentPosition = {'holding': False}
                # 止损
                elif row['最高'] > currentPosition['stop']:
                    currentPosition['outDate'] = row['日期']
                    currentPosition['outPrice'] = currentPosition['stop']
                    currentPosition['holdDays'] = (datetime.strptime(row['日期'], "%Y-%m-%d") - datetime.strptime(currentPosition['entryDate'], "%Y-%m-%d")).days
                    currentPosition['profitRatio'] = -1
                    currentPosition['isWin'] = False
                    isCrossing = False
                    isCrossed = False
                    isHigher = False
                    isLower = False
                    trading_list.append(currentPosition)
                    currentPosition = {'holding': False}
        else:
            # 判断是否满足入场条件
            # 1.均线多头或者空头排列
            ma1 = row[ma_column[0]]
            ma2 = row[ma_column[1]]
            ma3 = row[ma_column[2]]
            if (tradeDirection == 0 or tradeDirection == 2) and (ma1 < ma2 < ma3):
                isLower = True
                isHigher = False
            if (tradeDirection == 0 or tradeDirection == 1) and (ma1 > ma2 > ma3):
                isHigher = True
                isLower = False
            # 2.如果之前没有出现穿越布林带,判断是否穿过了布林带的上轨跟下轨(多头下轨,空头上轨)
            if isCrossed is False:
                # 穿过布林带,可能为入场位,记录下止损价
                if isLower:
                    # 判断上穿布林带
                    if row['最低'] <= row['higher_bound'] <= row['最高']:
                        isCrossing = True
                        currentPosition['stop'] = row['最高']
                        isCrossed = True
                if isHigher:
                    # 判断下穿布林带
                    if row['最低'] <= row['lower_bound'] <= row['最高']:
                        isCrossing = True
                        currentPosition['stop'] = row['最低']
                        isCrossed = True
            # 3.如果已经出现穿越,则看当前是否是收出了阳线(做多)或者阴线(做空),符合条件就进场
            # 进场条件为多头排列时,价格下穿布林带下轨后收出回到布林带中第一个阳线,空头排列时,价格上
            # 穿布林带上轨后收出回到布林带中第一个阴线
            else:
                # 出现了穿过布林带,判断当前是否还是正在布林带上,如果在,更新止损价格,如果回到布林带上并收反向K线进场,如果完全偏离出布林带放弃这次
                if isLower and isCrossing:
                    # K线最低价比布林带高,意思是离开了布林带,放弃
                    if row['最低'] > row['higher_bound']:
                        isCrossing = False
                        currentPosition['stop'] = 0
                        isCrossed = False
                    else:
                        # 只要收出阴线进场,阳线继续更新止损价
                        if row['开盘'] <= row['收盘']:
                            currentPosition['stop'] = max(row['最高'], currentPosition['stop'])
                        if row['开盘'] > row['收盘']:
                            currentPosition['stop'] = max(row['最高'], currentPosition['stop'])
                            currentPosition['holding'] = True
                            currentPosition['entryPrice'] = row['收盘']
                            currentPosition['direction'] = 'sell'
                            currentPosition['entryDate'] = row['日期']
                if isHigher and isCrossing:
                    # K线最高价比布林带低,意思是离开了布林带,放弃
                    if row['最高'] < row['lower_bound']:
                        isCrossing = False
                        currentPosition['stop'] = 0
                        isCrossed = False
                    else:
                        # 只要收出阳线进场,阴线继续更新止损价
                        if row['开盘'] >= row['收盘']:
                            currentPosition['stop'] = min(row['最低'], currentPosition['stop'])
                        if row['开盘'] < row['收盘']:
                            currentPosition['stop'] = min(row['最低'], currentPosition['stop'])
                            currentPosition['holding'] = True
                            currentPosition['entryPrice'] = row['收盘']
                            currentPosition['direction'] = 'buy'
                            currentPosition['entryDate'] = row['日期']
    # 计算总的交易频率跟胜率
    outResult = {}
    if(len(trading_list) <= 0):
        logger.info('[' + code + ']' + name + ':无交易数据,回测结束')
        return outResult
    result = pd.DataFrame(trading_list)
    outResult['code'] = code
    outResult['name'] = name
    # 总交易次数
    outResult['trade_times'] = len(result)
    # 盈利次数
    outResult['win_times'] = len(result[result['isWin'] == True])
    # 亏损次数
    outResult['lose_times'] = len(result[result['isWin'] == False])
    # 总盈利(盈亏比)
    outResult['profit_ratio'] = result['profitRatio'].sum()
    # 胜率
    outResult['win_chance'] = outResult['win_times']/outResult['trade_times'] * 100
    # 交易频率
    outResult['average_ransaction_requency'] = ((kdata.tail(1).index - kdata.head(1).index).days / outResult['trade_times']).values[0]
    # 做多次数
    outResult['buy_times'] = len(result[result['direction'] == 'buy'])
    # 做多盈利次数
    outResult['buy_win_times'] = len(result[(result['isWin'] == True) & (result['direction'] == 'buy')])
    # 做多亏损次数
    outResult['buy_lose_times'] = len(result[(result['isWin'] == False) & (result['direction'] == 'buy')])
    # 做空次数
    outResult['sell_times'] = len(result[result['direction'] == 'sell'])
    # 做空盈利次数
    outResult['sell_win_times'] = len(result[(result['isWin'] == True) & (result['direction'] == 'sell')])
    # 做空亏损次数
    outResult['sell_lose_times'] = len(result[(result['isWin'] == False) & (result['direction'] == 'sell')])
    # 最大连续亏损次数
    outResult['max_continuous_lose'] = calc.calc_field_value_times(result, 'isWin', False)

    outResult['trade_list'] = result
    logger.info('[' + code + ']' + name + ':回测结束')
    return outResult


def backtesting_all_stock(beginTime=None, endTime=None, tradeDirection=0):
    basic = pd.read_csv(ccons.stock_basic_file, dtype={'代码': str})
    summaryList = []
    for index in basic.index:
        row = basic.loc[index, :]
        s_code = row['代码']
        name = row['名称']
        try:
            out = backtesting_ma_bolling(s_code, name, beginTime, endTime, tradeDirection)
            if bool(out):
                stdout = '''总交易次数:{}, 盈利次数:{}, 亏损次数:{}, 总盈利(盈亏比):{}, 总胜率:{}%, 交易频率:{}/天, 多单次数:{}, 多单盈利次数:{}, 多单亏损次数:{}, 空单次数:{}, 空单盈利次数:{}, 空单亏损次数:{},最大连续亏损次数:{}.'''.format(out['trade_times'], out['win_times'], out['lose_times'], out['profit_ratio'], out['win_chance'], out['average_ransaction_requency'], out['buy_times'], out['buy_win_times'], out['buy_lose_times'], out['sell_times'], out['sell_win_times'], out['sell_lose_times'], out['max_continuous_lose'])
                logger.info('[' + out['code'] + ']' + out['name'] + '回测完成,统计结果:' + stdout)
                # logger.info('[' + out['code'] + ']' + out['name'] + '交易明细:')
                # logger.info(out['trade_list'])
                del out['trade_list']
                summaryList.append(out)
        except BaseException:
            logger.error(str(s_code) + ':回测失败,原因:' + traceback.format_exc())
    summary = pd.DataFrame(summaryList)
    summaryOut = '''总计,交易次数:{}, 盈利次数:{}, 亏损次数:{},  总盈利(盈亏比):{}, 总胜率:{}%'''.format(summary['trade_times'].sum(), summary['win_times'].sum(), summary['lose_times'].sum(), summary['profit_ratio'].sum(), summary['win_times'].sum()/summary['trade_times'].sum() * 100)
    logger.info(summaryOut)


if __name__ == '__main__':
    backtesting_all_stock(tradeDirection=1)
    # out = backtesting_ma_bolling('000001', tradeDirection=1)
    # if bool(out):
    #     stdout = '''总交易次数:{}, 盈利次数:{}, 亏损次数:{}, 总盈利(盈亏比):{}, 总胜率:{}%, 交易频率:{}/天, 多单次数:{}, 多单盈利次数:{}, 多单亏损次数:{}, 空单次数:{}, 空单盈利次数:{}, 空单亏损次数:{},最大连续亏损次数:{}.'''.format(out['trade_times'], out['win_times'], out['lose_times'], out['profit_ratio'], out['win_chance'], out['average_ransaction_requency'], out['buy_times'], out['buy_win_times'], out['buy_lose_times'], out['sell_times'], out['sell_win_times'], out['sell_lose_times'], out['max_continuous_lose'])
    #     logger.info('[' + out['code'] + ']' + out['name'] + '回测完成,统计结果:' + stdout)
    #     # logger.info('[' + out['code'] + ']' + out['name'] + '交易明细:')
    #     # logger.info(out['trade_list'])