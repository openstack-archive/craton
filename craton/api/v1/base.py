import functools
import inspect

from flask import g, jsonify, request
from oslo_serialization import jsonutils
import decorator
import flask_restful as restful

from craton import exceptions
from craton.api.v1.validators import request_validate, response_filter


class Resource(restful.Resource):
    method_decorators = [request_validate, response_filter]

    def error_response(self, status_code, message):
        resp = jsonify({
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


def filtered_context(query=None, filter_by=None, return_json=True):
    def decorator(f):
        objname = f.__qualname__.split('.')[0].rstrip('s').lower()

        @functools.wraps(f)
        def method_wrapper(self):
            context = request.environ.get("context")
            query_arg = g.args[query]
            if not query_arg:
                return self.error_response(
                    400, 'Missing `%s` in query' % query)
            filters = {}
            for key in filter_by:
                value = g.args.get(key)
                if value is not None:
                    filters[key] = value
            inspect.getmodule(f).LOG.info(
                "Getting all %s objects that match filters %s" % (
                    objname, filters))
            obj = f(self, context, query_arg, filters)
            if return_json:
                return jsonutils.to_primitive(obj), 200, None
            else:
                return None, 200, None

        return method_wrapper
    return decorator
