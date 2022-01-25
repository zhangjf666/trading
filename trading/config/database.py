"""
Date: 2021-01-14 22:00:56
Desc: 数据库操作
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Text, Date, DateTime, ForeignKey, UniqueConstraint, Index
from trading.config.logger import logger
import functools

Base = declarative_base()

# 以字典的形式配置好Mysql数据库的连接信息
mysql_dic = {
    'mysql_user': 'zjf',
    'mysql_pass': '39518605',
    'mysql_ip': '192.168.2.184',
    'mysql_port': 3306,
    'mysql_db': 'trading',
}


class Db(object):  # 创建一个专门连接数据库的类
    __instance = None
    __engine = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def gen_engine(self):
        if not Db.__engine:
            logger.info("初始化数据库引擎开始")
            mysql_str = "mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_ip}:{mysql_port}/{mysql_db}"  # 连接数据库的命令行
            mysql_con = mysql_str.format(**mysql_dic)  # 格式化命令
            engine = create_engine(mysql_con, max_overflow=5)  # 初始化数据库连接
            Db.__engine = engine
            logger.info("初始化数据库引擎成功")
        return Db.__engine

    def create_table(self):
        '''寻找Base的所有子类，按照子类的结构在数据库中生成对应的数据表信息'''
        self.gen_engine()
        Base.metadata.create_all(Db.__engine)

    @property
    def session(self):
        self.gen_engine()
        session = sessionmaker(bind=Db.__engine)
        return session()

    def get_connect(self):
        '''获取一个原生连接,需要手动关闭'''
        self.gen_engine()
        return Db.__engine.connect()


# 定义一个装饰器,包装其他调用自动获取session
def session_wrap(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        session = Db().session
        return method(*args, session, **kwargs)
    return wrapper


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
    em_rating_name = Column(String(100), comment='东方财富评级')
    s_rating_name = Column(String(100), comment='研究员评级')
    predict_this_year_eps = Column(String(100), comment='预测当年eps')
    predict_this_year_pe = Column(String(100), comment='预测当年pe')
    predict_next_year_eps = Column(String(100), comment='预测后一年eps')
    predict_next_year_pe = Column(String(100), comment='预测后一年pe')
    predict_next_two_year_eps = Column(String(100), comment='预测后二年eps')
    predict_next_two_year_pe = Column(String(100), comment='预测后二年pe')
    market = Column(String(50), comment='市场')
    category = Column(String(1), index=True, nullable=False, comment='研报分类(1:个股研报,2:行业研报,3:策略研报,4:宏观研报)')
