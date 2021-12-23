# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 策略路由
"""
import os
from flask import Blueprint
from pydantic import BaseModel
from web.api_exception import APIException
from web.api_route import route
import pandas as pd
import trading.collector.constant as ccons
import trading.strategy.constant as scons

strategy = Blueprint('strategy', __name__, url_prefix='/strategy')


@route(strategy, '/select-oversold-stock')
def select_oversold_stock():
    df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'stock.csv'), dtype={'代码': str})
    return df.to_dict(orient='records')


@route(strategy, '/sell-over-stock')
def sell_over_stock():
    df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'sell_stock.csv'), dtype={'代码': str})
    return df.to_dict(orient='records')


class StockMaRequest(BaseModel):
    miniTrendDay: int = 1
    maxTrendDay: int = 65535
    miniMarketValue: int = 1
    maxMarketValue: int = 65535
    industrys: list = None
    concepts: list = None


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
        result = df
    # 进行市值和持续天数排序
    result.sort_values(by=['持续天数', '流通市值'], ascending=[0, 0], inplace=True)
    result = result[(result['持续天数'] >= query.miniTrendDay) & (result['持续天数'] <= query.maxTrendDay)]
    result = result[(result['流通市值'] >= query.miniMarketValue * 100000000) & (result['流通市值'] <= query.maxMarketValue * 100000000)]
    return result.to_dict(orient='records')


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
    elif boardType == '2':
        df = pd.read_csv(os.path.join(scons.ma_higher_path, 'concept_index.csv'), dtype={'代码': str})
    else:
        raise APIException(400, '不支持的板块类型')
    df = df[(df['持续天数'] >= query.miniTrendDay) & (df['持续天数'] <= query.maxTrendDay)]
    return df.to_dict(orient='records')
