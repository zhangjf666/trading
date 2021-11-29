import json
from flask import Blueprint, Response
from api_response import APIResponse
from api_exception import APIException

exception = Blueprint('exception', __name__)


@exception.app_errorhandler(404)
def error_404(error):
    """这个handler可以catch住所有abort(404)以及找不到对应router的处理请求"""
    res = APIResponse(msg='找不到对应页面', code=404)
    return Response(json.dumps(res.body()), mimetype='application/json')


@exception.app_errorhandler(405)
def error_405(error):
    """这个handler可以catch住所有abort(405)以及请求方式有误的请求"""
    res = APIResponse(msg='请求方式有误', code=405)
    return Response(json.dumps(res.body()), mimetype='application/json')


@exception.app_errorhandler(Exception)
def error_500(error):
    """这个handler可以catch住所有的abort(500)和raise exeception."""
    if isinstance(error, APIException):
        return Response(error.get_body(), mimetype='application/json')
    res = APIResponse(msg='系统内部错误', code=500)
    return Response(json.dumps(res.body()), mimetype='application/json')
