from flask import json
from typing import List


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


class BaseFlaskPydanticException(Exception):
    """Base exc class for all exception from this library"""

    pass


class InvalidIterableOfModelsException(BaseFlaskPydanticException):
    """This exception is raised if there is a failure during serialization of
    response object with `response_many=True`"""

    pass


class JsonBodyParsingError(BaseFlaskPydanticException):
    """Exception for error occurring during parsing of request body"""

    pass


class ManyModelValidationError(BaseFlaskPydanticException):
    """This exception is raised if there is a failure during validation of many
    models in an iterable"""

    def __init__(self, errors: List[dict], *args):
        self._errors = errors
        super().__init__(*args)

    def errors(self):
        return self._errors
