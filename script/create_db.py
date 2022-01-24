# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 创建数据库表
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, Date, DateTime, ForeignKey, UniqueConstraint, Index


Base = declarative_base()


class ResearchReport(Base):
    __tablename__ = 'research_report'
    id = Column(Integer, primary_key=True, comment='自增id')
    title = Column(String(1000), index=True, nullable=False, comment='标题')
    stock_name = Column(String(100), index=True, comment='股票名称')
    stock_code = Column(String(10), index=True, comment='股票代码')
    page = Column(Integer, comment='页数')
    count = Column(Integer, comment='近一月报告数量')
    publish_date = Column(Date, index=True, nullable=False, comment='发布时间')
    researcher = Column(String(255), index=True, comment='研究员')
    summary = Column(Text, comment='摘要内容')
    source_url = Column(String(1000), comment='源链接地址')
    download_url = Column(String(1000), comment='下载地址')
    org_code = Column(String(10), comment='机构代码')
    org_name = Column(String(100), comment='机构名称')
    org_s_name = Column(String(20), index=True, comment='机构简称')
    industry_code = Column(String(20), comment='行业代码')
    industry_name = Column(String(50), index=True, comment='行业名称')
    em_rating_name = Column(String(10), comment='东方财富评级')
    s_rating_name = Column(String(10), comment='研究员评级')
    predict_this_year_eps = Column(String(100), comment='预测当年eps')
    predict_this_year_pe = Column(String(100), comment='预测当年pe')
    predict_next_year_eps = Column(String(100), comment='预测后一年eps')
    predict_next_year_pe = Column(String(100), comment='预测后一年pe')
    predict_next_two_year_eps = Column(String(100), comment='预测后二年eps')
    predict_next_two_year_pe = Column(String(100), comment='预测后二年pe')
    market = Column(String(50), comment='市场')
    category = Column(String(1), index=True, nullable=False, comment='研报分类(1:个股研报,2:行业研报,3:策略研报,4:宏观研报)')


# 1. 用sqlalchemy构建数据库链接engine
connect_info = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format("zjf", "39518605", "192.168.2.184", "3306", "trading")
engine = create_engine(connect_info)
# 2. 创建表
Base.metadata.create_all(engine)
