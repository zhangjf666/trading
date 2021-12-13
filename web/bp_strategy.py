"""
Date: 2021-11-29 22:00:56
Desc: 策略路由
"""
import os
import json
from flask import Blueprint, request
from pydantic import BaseModel
from matplotlib.pyplot import cla
from api_route import route
import pandas as pd
import trading.collector.constant as cons
import trading.strategy.constant as scons

strategy = Blueprint('strategy', __name__)


@route(strategy, '/strategy/select-oversold-stock')
def select_oversold_stock():
    df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'stock.csv'), dtype={'代码': str})
    return df.to_dict(orient='records')


@route(strategy, '/strategy/sell-over-stock')
def sell_over_stock():
    df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'sell.csv'), dtype={'代码': str})
    return df.to_dict(orient='records')


@route(strategy, '/strategy/stock-ma')
def stock_ma():
    df = pd.read_csv(os.path.join(scons.ma_higher_path, 'stock.csv'), dtype={'代码': str})
    return df.to_dict(orient='records')


class MaRequest(BaseModel):
    board: str


@route(strategy, '/strategy/index-ma', methods=['post'])
def index_ma(body: MaRequest):
    # board = request.get_json()['board']
    board = body.board
    df = pd.DataFrame()
    if board == '1':
        df = pd.read_csv(os.path.join(scons.ma_higher_path, 'industry_index.csv'), dtype={'代码': str})
    elif board == '2':
        df = pd.read_csv(os.path.join(scons.ma_higher_path, 'concept_index.csv'), dtype={'代码': str})
    return df.to_dict(orient='records')
