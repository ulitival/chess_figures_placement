"""
This module contains different helpers related to the API package
"""

import functools
from http import HTTPStatus

from flask import abort, request
from flask.wrappers import Response
from voluptuous import Invalid, Schema


def resp(content: str | bytes, status: int = HTTPStatus.OK, mimetype: str = "application/json"):
    """
    Produce response
    :param mimetype: A mime type of a returned content
    :param content: Response body (direct content or content chunks generator)
    :param status: Response status
    :return: JSON content type response object
    """
    return Response(content, status=status, mimetype=mimetype)


def expect(schema: Schema):
    """The helper function that serves as a decorator for Flask's endpoints. It utilizes
    voluptuous' Schema validator.

    :param Schema schema: an instal of a Schema class with defined validations
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kargs):
            req = getattr(request, "json")
            try:
                request_locs = schema(req)
            except Invalid as exc:
                abort(HTTPStatus.NOT_ACCEPTABLE, str(exc))
            kargs["valid_request"] = request_locs
            return func(*args, **kargs)

        return wrapper

    return decorator
