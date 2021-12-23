# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 采集路由
"""
from flask import Blueprint
from api_route import route
import pandas as pd
import trading.collector.constant as cons

collect = Blueprint('collect', __name__, url_prefix='/collect')


@route(collect, '/all-stock')
def all_stock_basic():
    df = pd.read_csv(cons.stock_basic_file, dtype={'代码': str})
    return df.to_dict(orient='records')


@route(collect, '/trade-day')
def trade_day():
    df = pd.read_csv(cons.stock_tradedate_file)
    return df['trade_date'].tolist()


@route(collect, '/convertible')
def convertible():
    df = pd.read_csv(cons.convertible_file)
    return df.to_dict(orient='records')


@route(collect, '/industry-list')
def industry_list():
    df = pd.read_csv(cons.industry_list_file)
    return df.to_dict(orient='records')


@route(collect, '/concept-list')
def concept_list():
    df = pd.read_csv(cons.concept_list_file)
    return df.to_dict(orient='records')


@route(collect, '/industry-stock')
def industry_stock():
    df = pd.read_csv(cons.industry_stocks_file)
    return df.to_dict(orient='records')


@route(collect, '/concept-stock')
def concept_stock():
    df = pd.read_csv(cons.concept_stocks_file)
    return df.to_dict(orient='records')
