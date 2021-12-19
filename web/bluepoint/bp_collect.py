# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 采集路由
"""
from flask import Blueprint
from flask_restplus import Resource, Namespace, fields
from api_route import route
from pydantic_validator import validate
from pydantic import BaseModel
import pandas as pd
import trading.collector.constant as cons

collect = Blueprint('collect', __name__, url_prefix='/collect')
ns = Namespace('collect', description='采集数据')


@ns.route('/all-stock')
class AllStockBasic(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(cons.stock_basic_file, dtype={'代码': str})
        return df.to_dict(orient='records')


@ns.route('/trade-day')
class TradeDay(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(cons.stock_tradedate_file)
        return df['trade_date'].tolist()


@ns.route('/convertible')
class Convertible(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(cons.convertible_file)
        return df.to_dict(orient='records')


@ns.route('/industry-list')
class IndustryList(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(cons.industry_list_file)
        return df.to_dict(orient='records')


@ns.route('/concept-list')
class ConceptList(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(cons.concept_list_file)
        return df.to_dict(orient='records')


@ns.route('/industry-stock')
class IndustryStock(Resource):
    @validate()
    def get(self):
        df = pd.read_csv(cons.industry_stocks_file)
        return df.to_dict(orient='records')


@ns.route('/concept-stock')
class ConceptStock(Resource):
    def get(self):
        df = pd.read_csv(cons.concept_stocks_file)
        return df.to_dict(orient='records')
