# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 策略路由
"""
import os
import json
from typing_extensions import Required
from flask import Blueprint, request
from numpy.core.numeric import normalize_axis_tuple
from pydantic import BaseModel
from matplotlib.pyplot import cla
from flask_restplus import Resource, Namespace, fields
from web.api_route import route
import pandas as pd
import trading.collector.constant as ccons
import trading.strategy.constant as scons
from pydantic_validator import validate

strategy = Blueprint('strategy', __name__, url_prefix='/strategy')
ns = Namespace('strategy', description='策略数据')


@ns.route('/select-oversold-stock')
class SelectOversoldStock(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'stock.csv'), dtype={'代码': str})
        return df.to_dict(orient='records')

@ns.route('/sell-over-stock')
class SellOverStock(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(os.path.join(scons.over_sold_new_stock_path, 'sell.csv'), dtype={'代码': str})
        return df.to_dict(orient='records')


@ns.route('/stock-ma')
class StockMa(Resource):
    class StockMaRequest(BaseModel):
        miniTrendDay: int = 1
        maxTrendDay: int = 65535
        miniMarketValue: int = 1
        maxMarketValue: int = 65535
        industrys: list = None
        concepts: list = None

    @validate()
    def get(self, query: StockMaRequest):
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


@ns.route('/index-ma')
class IndexMa(Resource):
    class IndexMaRequest(BaseModel):
        boardType: str
        miniTrendDay: int = 1
        maxTrendDay: int = 65535

    param = ns.model('IndexMaRequest', {
        'boardType': fields.String(description='1:行业板块,2概念板块', required=True),
        # 'miniTrendDay': fields.Integer(description='')
    })

    parser = ns.parser()
    parser.add_argument('boardType', location='args', help='1:行业板块,2概念板块')

    @ns.expect(parser)
    @validate()
    def get(self, query: IndexMaRequest):
        boardType = query.boardType
        df = pd.DataFrame()
        if boardType == '1':
            df = pd.read_csv(os.path.join(scons.ma_higher_path, 'industry_index.csv'), dtype={'代码': str})
        elif boardType == '2':
            df = pd.read_csv(os.path.join(scons.ma_higher_path, 'concept_index.csv'), dtype={'代码': str})
        df = df[(df['持续天数'] >= query.miniTrendDay) & (df['持续天数'] <= query.maxTrendDay)]
        return df.to_dict(orient='records')
