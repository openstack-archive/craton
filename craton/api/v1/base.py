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


def filtered_context(reserved_keys=None):
    def decorator(f):
        objname = f.__qualname__.split('.')[0].rstrip('s').lower()

        @functools.wraps(f)
        def method_wrapper(self):
            context = flask.request.environ.get("context")
            query_filters = {}
            for key in reserved_keys:
                value = flask.g.args.get(key)
                if value is not None:
                    query_filters[key] = value
            inspect.getmodule(f).LOG.info(
                "Getting all %s objects that match filters %s" % (
                    objname, query_filters))
            return f(self, context, **query_filters)

        return method_wrapper
    return decorator
