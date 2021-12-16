from functools import wraps
from typing import Any, Callable, Iterable, List, Optional, Tuple, Type, Union

from flask import Response, current_app, jsonify, make_response, request
from pydantic import BaseModel, ValidationError
from pydantic.tools import parse_obj_as

from api_exception import (
    InvalidIterableOfModelsException,
    JsonBodyParsingError,
    ManyModelValidationError,
)

from werkzeug.datastructures import ImmutableMultiDict
from api_exception import APIException

try:
    from flask_restful import original_flask_make_response as make_response
except ImportError:
    pass


def convert_query_params(
    query_params: ImmutableMultiDict, model: Type[BaseModel]
) -> dict:
    """
    group query parameters into lists if model defines them

    :param query_params: flasks request.args
    :param model: query parameter's model
    :return: resulting parameters
    """
    return {
        **query_params.to_dict(),
        **{
            key: value
            for key, value in query_params.to_dict(flat=False).items()
            if key in model.__fields__ and model.__fields__[key].is_complex()
        },
    }


def make_json_response(
    content: Union[BaseModel, Iterable[BaseModel]],
    status_code: int,
    by_alias: bool,
    exclude_none: bool = False,
    many: bool = False,
) -> Response:
    """serializes model, creates JSON response with given status code"""
    if many:
        js = f"[{', '.join([model.json(exclude_none=exclude_none, by_alias=by_alias) for model in content])}]"
    else:
        js = content.json(exclude_none=exclude_none, by_alias=by_alias)
    response = make_response(js, status_code)
    response.mimetype = "application/json"
    return response


def unsupported_media_type_response(request_cont_type: str) -> Response:
    body = f"Unsupported media type '{request_cont_type}' in request. 'application/json' is required."
    raise APIException(405, body)


def is_iterable_of_models(content: Any) -> bool:
    try:
        return all(isinstance(obj, BaseModel) for obj in content)
    except TypeError:
        return False


def validate_many_models(model: Type[BaseModel], content: Any) -> List[BaseModel]:
    try:
        return [model(**fields) for fields in content]
    except TypeError:
        # iteration through `content` fails
        err = [
            {
                "loc": ["root"],
                "msg": "is not an array of objects",
                "type": "type_error.array",
            }
        ]
        raise ManyModelValidationError(err)
    except ValidationError as ve:
        raise ManyModelValidationError(ve.errors())


def validate_path_params(func: Callable, kwargs: dict) -> Tuple[dict, list]:
    errors = []
    validated = {}
    for name, type_ in func.__annotations__.items():
        if name in {"query", "body", "return"}:
            continue
        try:
            value = parse_obj_as(type_, kwargs.get(name))
            validated[name] = value
        except ValidationError as e:
            err = e.errors()[0]
            err["loc"] = [name]
            errors.append(err)
    kwargs = {**kwargs, **validated}
    return kwargs, errors


def get_body_dict(**params):
    data = request.get_json(**params)
    if data is None and params.get("silent"):
        return {}
    return data


def validate(
    body: Optional[Type[BaseModel]] = None,
    query: Optional[Type[BaseModel]] = None,
    on_success_status: int = 200,
    exclude_none: bool = False,
    response_many: bool = False,
    request_body_many: bool = False,
    response_by_alias: bool = False,
    get_json_params: Optional[dict] = None,
):
    """
    Decorator for route methods which will validate query and body parameters
    as well as serialize the response (if it derives from pydantic's BaseModel
    class).

    Request parameters are accessible via flask's `request` variable:
        - request.query_params
        - request.body_params

    Or directly as `kwargs`, if you define them in the decorated function.

    `exclude_none` whether to remove None fields from response
    `response_many` whether content of response consists of many objects
        (e. g. List[BaseModel]). Resulting response will be an array of serialized
        models.
    `request_body_many` whether response body contains array of given model
        (request.body_params then contains list of models i. e. List[BaseModel])
    `response_by_alias` whether Pydantic's alias is used
    `get_json_params` - parameters to be passed to Request.get_json() function

    example::

        from flask import request
        from flask_pydantic import validate
        from pydantic import BaseModel

        class Query(BaseModel):
            query: str

        class Body(BaseModel):
            color: str

        class MyModel(BaseModel):
            id: int
            color: str
            description: str

        ...

        @app.route("/")
        @validate(query=Query, body=Body)
        def test_route():
            query = request.query_params.query
            color = request.body_params.query

            return MyModel(...)

        @app.route("/kwargs")
        @validate()
        def test_route_kwargs(query:Query, body:Body):

            return MyModel(...)

    -> that will render JSON response with serialized MyModel instance
    """

    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            q, b, err = None, None, {}
            kwargs, path_err = validate_path_params(func, kwargs)
            if path_err:
                err["path_params"] = path_err
            query_in_kwargs = func.__annotations__.get("query")
            query_model = query_in_kwargs or query
            if query_model:
                query_params = convert_query_params(request.args, query_model)
                try:
                    q = query_model(**query_params)
                except ValidationError as ve:
                    err["query_params"] = ve.errors()
            body_in_kwargs = func.__annotations__.get("body")
            body_model = body_in_kwargs or body
            if body_model:
                body_params = get_body_dict(**(get_json_params or {}))
                if "__root__" in body_model.__fields__:
                    try:
                        b = body_model(__root__=body_params).__root__
                    except ValidationError as ve:
                        err["body_params"] = ve.errors()
                elif request_body_many:
                    try:
                        b = validate_many_models(body_model, body_params)
                    except ManyModelValidationError as e:
                        err["body_params"] = e.errors()
                else:
                    try:
                        b = body_model(**body_params)
                    except TypeError:
                        content_type = request.headers.get("Content-Type", "").lower()
                        media_type = content_type.split(";")[0]
                        if media_type != "application/json":
                            return unsupported_media_type_response(content_type)
                        else:
                            raise JsonBodyParsingError()
                    except ValidationError as ve:
                        err["body_params"] = ve.errors()
            request.query_params = q
            request.body_params = b
            if query_in_kwargs:
                kwargs["query"] = q
            if body_in_kwargs:
                kwargs["body"] = b

            if err:
                status_code = current_app.config.get(
                    "FLASK_PYDANTIC_VALIDATION_ERROR_STATUS_CODE", 400
                )
                msg = ''
                for key in err:
                    err_param = err[key]
                    for item in err_param:
                        msg = msg + 'name={0},msg={1};'.format(','.join(str(i) for i in item['loc']), item['msg'])
                raise APIException(status_code, msg)
            res = func(*args, **kwargs)

            if response_many:
                if is_iterable_of_models(res):
                    return make_json_response(
                        res,
                        on_success_status,
                        by_alias=response_by_alias,
                        exclude_none=exclude_none,
                        many=True,
                    )
                else:
                    raise InvalidIterableOfModelsException(res)

            if isinstance(res, BaseModel):
                return make_json_response(
                    res,
                    on_success_status,
                    exclude_none=exclude_none,
                    by_alias=response_by_alias,
                )

            if (
                isinstance(res, tuple)
                and len(res) == 2
                and isinstance(res[0], BaseModel)
            ):
                return make_json_response(
                    res[0],
                    res[1],
                    exclude_none=exclude_none,
                    by_alias=response_by_alias,
                )

            return res

        return wrapper

    return decorate