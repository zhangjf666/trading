"""
Date: 2021-11-29 22:00:56
Desc: 路由装饰器
"""
from traceback import print_exc
from flask import jsonify
from functools import wraps

from api_response import APIResponse
from flask_pydantic import validate


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @validate()
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            res = APIResponse(data=result)
            return jsonify(res.body())
        return f
    return decorator
