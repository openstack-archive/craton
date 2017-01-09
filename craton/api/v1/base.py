import functools
import inspect

import decorator

import flask
import flask_restful as restful

from craton.api.v1.validators import ensure_project_exists
from craton.api.v1.validators import request_validate
from craton.api.v1.validators import response_filter
from craton import exceptions


class Resource(restful.Resource):
    method_decorators = [request_validate, ensure_project_exists,
                         response_filter]

    def error_response(self, status_code, message):
        resp = flask.jsonify({
            'status': status_code,
            'message': message
            })
        resp.status_code = status_code
        return resp


@decorator.decorator
def http_codes(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except exceptions.Base as err:
        return args[0].error_response(err.code, err.message)
    except Exception as err:
        inspect.getmodule(f).LOG.error(
            'Error during %s: %s' % (f.__qualname__, err))
        return args[0].error_response(500, 'Unknown Error')


def pagination_context(function):
    @functools.wraps(function)
    def wrapper(self, context, request_args):
        pagination_parameters = {
            'limit': limit_from(request_args),
            'marker': request_args.pop('marker', None),
        }
        return function(context, request_args=request_args,
                        pagination_params=pagination_parameters)
    return wrapper


def limit_from(filters, minimum=10, default=30, maximum=100):
    """Retrieve the limit from query filters."""
    limit_str = filters.pop('limit', None)

    if limit_str is None:
        return default

    limit = int(limit_str)

    # NOTE(sigmavirus24): If our limit falls within in our constraints, just
    # return that
    if minimum <= limit <= maximum:
        return limit

    if limit < minimum:
        return minimum

    # NOTE(sigmavirus24): If our limit isn't within the constraints, and it
    # isn't too small, then it must be too big. In that case, let's just
    # return the maximum.
    return maximum
