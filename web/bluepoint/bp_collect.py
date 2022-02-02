# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 采集路由
"""
import os
import json
from unicodedata import category
from flask import Blueprint
from pydantic import BaseModel
from sqlalchemy import and_, or_
from web.api_exception import APIException
from api_route import route
import pandas as pd
import trading.collector.constant as cons
import trading.util.common_util as cutil
import models as Models
from ext import db
import web_util as wutil
from sqlalchemy.dialects import mysql

collect = Blueprint('collect', __name__, url_prefix='/collect')


@route(collect, '/all-stock')
def all_stock_basic():
    df = pd.read_csv(cons.stock_basic_file, dtype={'代码': str})
    return cutil.to_json(df)


@route(collect, '/trade-day')
def trade_day():
    df = pd.read_csv(cons.stock_tradedate_file)
    return df['trade_date'].values.tolist() if df.shape[0] > 0 else []


class ConvertibleRequest(BaseModel):
    miniDoubleValue: int = 0
    maxDoubleValue: int = 1000000
    miniBondPrice: int = 0
    maxBondPrice: int = 100000


@route(collect, '/convertible')
def convertible(query: ConvertibleRequest):
    result = pd.read_csv(cons.convertible_file)
    result = result[(result['双低值'] >= query.miniDoubleValue)
                    & (result['双低值'] <= query.maxDoubleValue)]
    result = result[(result['转债最新价'] >= query.miniBondPrice)
                    & (result['转债最新价'] <= query.maxBondPrice)]
    result.sort_values(by=['双低值'], ascending=[True], inplace=True)
    return cutil.to_json(result)


@route(collect, '/industry-list')
def industry_list():
    df = pd.read_csv(cons.industry_list_file)
    return cutil.to_json(df)


@route(collect, '/concept-list')
def concept_list():
    df = pd.read_csv(cons.concept_list_file)
    return cutil.to_json(df)


@route(collect, '/industry-stock')
def industry_stock():
    df = pd.read_csv(cons.industry_stocks_file, dtype={'代码': str})
    return cutil.to_json(df)


@route(collect, '/concept-stock')
def concept_stock():
    df = pd.read_csv(cons.concept_stocks_file, dtype={'代码': str})
    return cutil.to_json(df)


class JgdytjQuery(BaseModel):
    beginDate: str
    endDate: str


# 机构调研统计
@route(collect, '/jgdytj')
def jgdytj(query: JgdytjQuery):
    df = pd.read_csv(cons.jgdytj_file, dtype={'代码': str})
    df = df[(df['接待日期'] >= query.beginDate) & (df['接待日期'] <= query.endDate)]
    df.sort_values(by='接待日期', ascending=False, inplace=True)
    return cutil.to_json(df)


# 技术指标
class JszbQuery(BaseModel):
    zbType: str
    beginDate: str
    endDate: str


@route(collect, '/jszb')
def jszb_cxg(query: JszbQuery):
    # 创新高
    if query.zbType == 'cxg':
        df = pd.read_csv(cons.cxg_file, dtype={'代码': str})
        df = df[(df['日期'] >= query.beginDate) & (df['日期'] <= query.endDate)]
        df.sort_values(by='日期', ascending=False, inplace=True)
    # 创新低
    elif query.zbType == 'cxd':
        df = pd.read_csv(cons.cxd_file, dtype={'代码': str})
        df = df[(df['日期'] >= query.beginDate) & (df['日期'] <= query.endDate)]
        df.sort_values(by='日期', ascending=False, inplace=True)
    # 连续上涨
    elif query.zbType == 'lxsz':
        df = pd.read_csv(cons.lxsz_file, dtype={'代码': str})
    # 连续下跌
    elif query.zbType == 'lxxd':
        df = pd.read_csv(cons.lxxd_file, dtype={'代码': str})
    # 持续放量
    elif query.zbType == 'cxfl':
        df = pd.read_csv(cons.cxfl_file, dtype={'代码': str})
    # 持续缩量
    elif query.zbType == 'cxsl':
        df = pd.read_csv(cons.cxsl_file, dtype={'代码': str})
    # 量价齐升
    elif query.zbType == 'ljqs':
        df = pd.read_csv(cons.ljqs_file, dtype={'代码': str})
    # 量价齐跌
    elif query.zbType == 'ljqd':
        df = pd.read_csv(cons.ljqd_file, dtype={'代码': str})
    else:
        raise APIException(400, '不支持的技术指标类型')
    return cutil.to_json(df)


# 资金流向
class ZjlxQuery(BaseModel):
    zjType: str = '0'
    bdType: str = '3'


@route(collect, '/zjlx')
def zjlx(query: ZjlxQuery):
    file_name = ''
    if query.zjType == '0':
        if query.bdType == '0':
            file_name = 'ggzj-当日排行.csv'
        elif query.bdType == '3':
            file_name = 'ggzj-3日排行.csv'
        elif query.bdType == '5':
            file_name = 'ggzj-5日排行.csv'
        elif query.bdType == '10':
            file_name = 'ggzj-10日排行.csv'
        elif query.bdType == '20':
            file_name = 'ggzj-20日排行.csv'
        else:
            raise APIException(400, '不支持的资金流向类型')
    elif query.zjType == '1':
        if query.bdType == '0':
            file_name = 'gnzj-当日排行.csv'
        elif query.bdType == '3':
            file_name = 'gnzj-3日排行.csv'
        elif query.bdType == '5':
            file_name = 'gnzj-5日排行.csv'
        elif query.bdType == '10':
            file_name = 'gnzj-10日排行.csv'
        elif query.bdType == '20':
            file_name = 'gnzj-20日排行.csv'
        else:
            raise APIException(400, '不支持的资金流向类型')
    elif query.zjType == '2':
        if query.bdType == '0':
            file_name = 'hyzj-当日排行.csv'
        elif query.bdType == '3':
            file_name = 'hyzj-3日排行.csv'
        elif query.bdType == '5':
            file_name = 'hyzj-5日排行.csv'
        elif query.bdType == '10':
            file_name = 'hyzj-10日排行.csv'
        elif query.bdType == '20':
            file_name = 'hyzj-20日排行.csv'
        else:
            raise APIException(400, '不支持的资金流向类型')
    else:
        raise APIException(400, '不支持的资金流向类型')
    df = pd.read_csv(os.path.join(cons.zjlx_path, file_name),
                     dtype={'代码': str})
    return cutil.to_json(df)


class YjbgQuery(BaseModel):
    context: str = None
    stockName: str = None
    stockCode: str = None
    researcher: str = None
    orgName: str = None
    industryName: str = None
    minPage: str = None
    beginDate: str = None
    endDate: str = None
    category: list = None
    page: int = 1
    perPage: int = 10


@route(collect, '/yjbg')
def yjbg(query: YjbgQuery):
    session = db.session.query(Models.ResearchReport)
    # 查询条件组合
    search = or_
    if query.context:
        word = query.context.split()
        for key in word:
            if key.isdigit():
                search = or_(search, Models.ResearchReport.stock_code == key)
            else:
                search = or_(
                    search,
                    Models.ResearchReport.title.like('%{}%'.format(key)),
                    Models.ResearchReport.stock_name.like('%{}%'.format(key)),
                    Models.ResearchReport.industry_name.like('%{}%'.format(key)),
                    Models.ResearchReport.researcher.like('%{}%'.format(key)))
    if query.stockCode:
        search = or_(search, Models.ResearchReport.stock_code == query.stockCode)
    if query.stockName:
        search = or_(search, Models.ResearchReport.stock_name.like('%{}%'.format(query.stockName)))
    if query.researcher:
        search = or_(search, Models.ResearchReport.researcher.like('%{}%'.format(query.researcher)))
    if query.industryName:
        search = or_(search, Models.ResearchReport.industry_name.like('%{}%'.format(query.industryName)))
    if query.orgName:
        search = or_(search, Models.ResearchReport.org_s_name.like('%{}%'.format(query.orgName)))
    if query.beginDate:
        search = and_(search, Models.ResearchReport.publish_date >= query.beginDate)
    if query.endDate:
        search = and_(search, Models.ResearchReport.publish_date <= query.endDate)
    if query.minPage:
        search = and_(search, Models.ResearchReport.page >= query.minPage)
    if query.category:
        search = and_(search, Models.ResearchReport.category.in_(query.category))
    page = session.filter(search).order_by(
        Models.ResearchReport.publish_date.desc(), Models.ResearchReport.category.asc()).paginate(query.page, query.perPage)
    # print(str(session.statement.compile(dialect=mysql.dialect(),compile_kwargs={"literal_binds": True})))
    res = wutil.page_to_dict(page)
    rr_schema = Models.ResearchReportSchema(many=True)
    res['items'] = rr_schema.dump(res['items'])
    return res
