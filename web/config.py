
# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: flask配置
"""

from trading.config.database import db_str
# 数据库链接的配置，此项必须，格式为（数据库+驱动://用户名:密码@数据库主机地址:端口/数据库名称）
SQLALCHEMY_DATABASE_URI = db_str
# 跟踪对象的修改，在本例中用不到调高运行效率，所以设置为False
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 打印sql语句
SQLALCHEMY_ECHO = True
# 开启Debug
DEBUG = True
# 模板自动加载
TEMPLATES_AUTO_RELOAD = True
