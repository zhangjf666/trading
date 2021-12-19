# -*- coding:utf-8 -*-
"""
Date: 2021-11-29 22:00:56
Desc: flask服务端
"""
import json
from flask import Flask
from flask.helpers import make_response
from web.bluepoint.bp_collect import collect, ns as col_ns
from web.bluepoint.bp_strategy import strategy, ns as str_ns
from web.bluepoint.bp_exception import exception
from api_response import APIResponse
from flask_restplus import Api

app = Flask('trading-web')
api = Api(app)
# 禁用api文档
# api._doc = False
api.add_namespace(str_ns)
api.add_namespace(col_ns)

# 注册蓝图
app.register_blueprint(exception)
app.register_blueprint(collect)
app.register_blueprint(strategy)


# 统一返回内容
@api.representation('application/json')
def response(data, code, headers=None):
    if isinstance(data, dict) and data['swagger']:
        resp = make_response(data, code)
    else:
        resp = make_response(json.dumps(APIResponse(data=data).body()), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True)
