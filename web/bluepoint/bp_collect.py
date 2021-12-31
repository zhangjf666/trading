# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 采集路由
"""
from flask import Blueprint
from pydantic import BaseModel
from api_route import route
import pandas as pd
import trading.collector.constant as cons

collect = Blueprint('collect', __name__, url_prefix='/collect')


@route(collect, '/all-stock')
def all_stock_basic():
    df = pd.read_csv(cons.stock_basic_file, dtype={'代码': str})
    return df.to_dict(orient='records') if df.shape[0] > 0 else []


@route(collect, '/trade-day')
def trade_day():
    df = pd.read_csv(cons.stock_tradedate_file)
    return df.to_dict(orient='records') if df.shape[0] > 0 else []


class ConvertibleRequest(BaseModel):
    miniDoubleValue: int = 0
    maxDoubleValue: int = 1000000
    miniBondPrice: int = 0
    maxBondPrice: int = 100000


@route(collect, '/convertible')
def convertible(query: ConvertibleRequest):
    result = pd.read_csv(cons.convertible_file)
    result = result[(result['双低值'] >= query.miniDoubleValue) & (result['双低值'] <= query.maxDoubleValue)]
    result = result[(result['转债最新价'] >= query.miniBondPrice) & (result['转债最新价'] <= query.maxBondPrice)]
    result.sort_values(by=['双低值'], ascending=[True], inplace=True)
    return result.to_dict(orient='records') if result.shape[0] > 0 else []


@route(collect, '/industry-list')
def industry_list():
    df = pd.read_csv(cons.industry_list_file)
    return df.to_dict(orient='records') if df.shape[0] > 0 else []


@route(collect, '/concept-list')
def concept_list():
    df = pd.read_csv(cons.concept_list_file)
    return df.to_dict(orient='records') if df.shape[0] > 0 else []


@route(collect, '/industry-stock')
def industry_stock():
    df = pd.read_csv(cons.industry_stocks_file)
    return df.to_dict(orient='records') if df.shape[0] > 0 else []


@route(collect, '/concept-stock')
def concept_stock():
    df = pd.read_csv(cons.concept_stocks_file)
    return df.to_dict(orient='records') if df.shape[0] > 0 else []
