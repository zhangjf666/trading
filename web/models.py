# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 数据库模型
"""

from ext import db
from ext import ma


class ResearchReport(db.Model):
    __tablename__ = 'research_report'
    id = db.Column(db.Integer, primary_key=True, comment='自增id')
    title = db.Column(db.String(1000), index=True, nullable=False, comment='标题')
    stock_name = db.Column(db.String(100), index=True, comment='股票名称')
    stock_code = db.Column(db.String(10), index=True, comment='股票代码')
    page = db.Column(db.Integer, comment='页数')
    count = db.Column(db.Integer, comment='近一月报告数量')
    publish_date = db.Column(db.Date, index=True, nullable=False, comment='发布时间')
    researcher = db.Column(db.String(255), index=True, comment='研究员')
    summary = db.Column(db.Text, comment='摘要内容')
    source_url = db.Column(db.String(1000), comment='源链接地址')
    download_url = db.Column(db.String(1000), comment='下载地址')
    org_code = db.Column(db.String(10), comment='机构代码')
    org_name = db.Column(db.String(100), comment='机构名称')
    org_s_name = db.Column(db.String(20), index=True, comment='机构简称')
    industry_code = db.Column(db.String(20), comment='行业代码')
    industry_name = db.Column(db.String(50), index=True, comment='行业名称')
    em_rating_name = db.Column(db.String(100), comment='东方财富评级')
    s_rating_name = db.Column(db.String(100), comment='研究员评级')
    predict_this_year_eps = db.Column(db.String(100), comment='预测当年eps')
    predict_this_year_pe = db.Column(db.String(100), comment='预测当年pe')
    predict_next_year_eps = db.Column(db.String(100), comment='预测后一年eps')
    predict_next_year_pe = db.Column(db.String(100), comment='预测后一年pe')
    predict_next_two_year_eps = db.Column(db.String(100), comment='预测后二年eps')
    predict_next_two_year_pe = db.Column(db.String(100), comment='预测后二年pe')
    market = db.Column(db.String(50), comment='市场')
    category = db.Column(db.String(1), index=True, nullable=False, comment='研报分类(1:个股研报,2:行业研报,3:策略研报,4:宏观研报)')


class ResearchReportSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ResearchReport
    id = ma.auto_field()
    title = ma.auto_field()
    stock_name = ma.auto_field()
    stock_code = ma.auto_field()
    page = ma.auto_field()
    count = ma.auto_field()
    publish_date = ma.auto_field()
    researcher = ma.auto_field()
    summary = ma.auto_field()
    download_url = ma.auto_field()
    org_code = ma.auto_field()
    org_name = ma.auto_field()
    org_s_name = ma.auto_field()
    industry_code = ma.auto_field()
    industry_name = ma.auto_field()
    em_rating_name = ma.auto_field()
    s_rating_name = ma.auto_field()
    predict_this_year_eps = ma.auto_field()
    predict_this_year_pe = ma.auto_field()
    predict_next_year_eps = ma.auto_field()
    predict_next_year_pe = ma.auto_field()
    predict_next_two_year_eps = ma.auto_field()
    predict_next_two_year_pe = ma.auto_field()
    market = ma.auto_field()
    category = ma.auto_field()
