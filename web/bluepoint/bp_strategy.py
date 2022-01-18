# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 策略路由
"""
from datetime import date
import os
import traceback
from flask import Blueprint
from markupsafe import re
from pydantic import BaseModel
from web.api_exception import APIException
from web.api_route import route
import pandas as pd
import trading.collector.constant as ccons
import trading.strategy.constant as scons
import trading.strategy.n2s as tsn
import trading.util.common_util as cutil
from trading.config.logger import logger

strategy = Blueprint('strategy', __name__, url_prefix='/strategy')


class OverSoldRequest(BaseModel):
    beginDate: str
    endDate: str


@route(strategy, '/select-oversold-stock')
def select_oversold_stock(query: OverSoldRequest):
    df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'stock.csv'), dtype={'代码': str})
    df = df[(df['日期'] >= query.beginDate) & (df['日期'] <= query.endDate)]
    df.sort_values(by='日期', ascending=False, inplace=True)
    df['总市值'] = (df['总市值'].astype(float)/100000000).round(2)
    df['流通市值'] = (df['流通市值'].astype(float)/100000000).round(2)
    df.rename(columns={'总市值': '总市值(亿)', '流通市值': '流通市值(亿)'}, inplace=True)
    return cutil.to_json(df)


@route(strategy, '/sell-over-stock')
def sell_over_stock(query: OverSoldRequest):
    df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'sell_stock.csv'), dtype={'代码': str})
    df = df[(df['日期'] >= query.beginDate) & (df['日期'] <= query.endDate)]
    df.sort_values(by='日期', ascending=False, inplace=True)
    df['涨幅'] = (df['涨幅'].astype(float) * 100).round(2)
    df['跌幅'] = (df['跌幅'].astype(float) * 100).round(2)
    df.rename(columns={'涨幅': '涨幅(%)', '跌幅': '跌幅(%)'}, inplace=True)
    return cutil.to_json(df)


class StockMaRequest(BaseModel):
    miniTrendDay: int = 1
    maxTrendDay: int = 65535
    miniMarketValue: int = 1
    maxMarketValue: int = 65535
    industrys: list = None
    concepts: list = None
    jszb: list = None


@route(strategy, '/stock-ma')
def stock_ma(query: StockMaRequest):
    result = pd.DataFrame()
    df = pd.read_csv(scons.ma_higher_stock_file, dtype={'代码': str})
    # 筛选行业
    if query.industrys:
        ind_df = pd.read_csv(ccons.industry_stocks_file, dtype={'行业代码': str, '代码': str})
        ind_df = ind_df[ind_df['行业代码'].isin(query.industrys)]
        result = result.append(df[df['代码'].isin(ind_df['代码'])])
    # 筛选概念
    if query.concepts:
        con_df = pd.read_csv(ccons.concept_stocks_file, dtype={'概念代码': str, '代码': str})
        con_df = con_df[con_df['概念代码'].isin(query.concepts)]
        result = result.append(df[df['代码'].isin(con_df['代码'])])
    if len(result) == 0:
        if query.industrys or query.concepts:
            return cutil.to_json(result)
        else:
            result = df
    # 叠加技术指标
    if query.jszb:
        for zb in query.jszb:
            try:
                zb_df = pd.read_csv(os.path.join(ccons.jszb_path, zb + ccons.file_type_csv), dtype={'代码': str})
                result = result[result['代码'].isin(zb_df['代码'])]
            except BaseException:
                logger.info('叠加技术指标' + zb + '出错:' + traceback.print_exc())
    # 进行市值和持续天数排序
    result.drop_duplicates(inplace=True)
    result.sort_values(by=['持续天数', '流通市值'], ascending=[False, False], inplace=True)
    result = result[(result['持续天数'] >= query.miniTrendDay) & (result['持续天数'] <= query.maxTrendDay)]
    result = result[(result['流通市值'] >= query.miniMarketValue * 100000000) & (result['流通市值'] <= query.maxMarketValue * 100000000)]
    result['总市值'] = (result['总市值'].astype(float)/100000000).round(2)
    result['流通市值'] = (result['流通市值'].astype(float)/100000000).round(2)
    result.rename(columns={'总市值': '总市值(亿)', '流通市值': '流通市值(亿)'}, inplace=True)
    return cutil.to_json(result)


class IndexMaRequest(BaseModel):
    boardType: str
    miniTrendDay: int = 1
    maxTrendDay: int = 65535


@route(strategy, '/index-ma')
def IndexMa(query: IndexMaRequest):
    boardType = query.boardType
    df = pd.DataFrame()
    if boardType == '1':
        df = pd.read_csv(os.path.join(scons.ma_higher_path, 'industry_index.csv'), dtype={'代码': str})
        df.insert(0, '指数类型', '行业指数')
    elif boardType == '2':
        df = pd.read_csv(os.path.join(scons.ma_higher_path, 'concept_index.csv'), dtype={'代码': str})
        df.insert(0, '指数类型', '概念指数')
    elif boardType == '3':
        idf = pd.read_csv(os.path.join(scons.ma_higher_path, 'industry_index.csv'), dtype={'代码': str})
        idf.insert(0, '指数类型', '行业指数')
        df = idf
        cdf = pd.read_csv(os.path.join(scons.ma_higher_path, 'concept_index.csv'), dtype={'代码': str})
        cdf.insert(0, '指数类型', '概念指数')
        df = df.append(cdf)
    else:
        raise APIException(400, '不支持的板块类型')
    df = df[(df['持续天数'] >= query.miniTrendDay) & (df['持续天数'] <= query.maxTrendDay)]
    df.sort_values(by=['持续天数'], ascending=[False], inplace=True)
    df['成交量'] = (df['成交量'].astype(float)/100000000).round(2)
    df['成交额'] = (df['成交额'].astype(float)/100000000).round(2)
    df.rename(columns={'成交量': '成交量(亿)', '成交额': '成交额(亿)'}, inplace=True)
    return cutil.to_json(df)


class N2sSignRequest(BaseModel):
    multiple: float = 2
    period: int = 252


@route(strategy, '/n2s-sign')
def N2sSign(query: N2sSignRequest):
    df = tsn.show_n2s_sign(multiple=query.multiple, period=query.period)
    return cutil.to_json(df)


class N2sSignTestRequest(BaseModel):
    code: str
    codeType: str = 0
    startDate: str
    endDate: str
    multiple: float = 2
    period: int = 252


@route(strategy, '/n2s-sign-test')
def N2sSignTestData(query: N2sSignTestRequest):
    result = tsn.get_n2s_strategy_detail(code=query.code, code_type=query.codeType, start_date=query.startDate, end_date=query.endDate, multiple=query.multiple, period=query.period)
    return result
