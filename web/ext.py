# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: 解决循环依赖
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()
