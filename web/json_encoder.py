from flask.json import JSONEncoder as BaseJSONEncoder

import datetime
import decimal


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H-%M-%S')
        if isinstance(o, decimal.Decimal):
            return float(o)
        # 其他

        return super(JSONEncoder, self).default(o)
