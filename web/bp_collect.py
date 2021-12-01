"""
Date: 2021-11-29 22:00:56
Desc: 采集路由
"""
from flask import Blueprint
from api_route import route
import pandas as pd
import trading.collector.constant as cons

collect = Blueprint('collect', __name__)


@route(collect, '/collect/all-stock')
def all_stock_basic():
    basic = pd.read_csv(cons.stock_basic_file, dtype={'代码': str})
    return basic.to_dict(orient='records')


@route(collect, '/collect/trade-day')
def trade_day():
    df = pd.read_csv(cons.stock_tradedate_file)
    return df['trade_date'].tolist()