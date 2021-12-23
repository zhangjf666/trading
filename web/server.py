# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: flask服务端
"""
from flask import Flask
from web.bluepoint.bp_collect import collect
from web.bluepoint.bp_strategy import strategy
from web.bluepoint.bp_exception import exception

app = Flask('trading-web')

# 注册蓝图
app.register_blueprint(exception)
app.register_blueprint(collect)
app.register_blueprint(strategy)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True)
