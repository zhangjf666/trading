class APIResponse():
    msg = 'ok'
    code = 0
    data = {}

    def __init__(self, code=0, msg='ok', data=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data

    def body(self):
        body = {}
        body['data'] = self.data
        body['msg'] = self.msg
        body['code'] = self.code

        return body
