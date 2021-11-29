from flask import json


class APIException(Exception):
    code = 500
    msg = 'server error'

    def __init__(self, code=None, msg=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg

    def get_body(self, environ=None):
        body = {'msg': self.msg, 'code': self.code}
        text = json.dumps(body)
        return text
