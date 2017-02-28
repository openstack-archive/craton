import functools
import inspect
import re
import urllib.parse as urllib

import decorator

import flask
import flask_restful as restful
from oslo_serialization import jsonutils

from craton.api.v1.resources import utils
from craton.api.v1.validators import ensure_project_exists
from craton.api.v1.validators import request_validate
from craton.api.v1.validators import response_filter
from craton import exceptions


SORT_KEY_SPLITTER = re.compile('[ ,]')


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


def get_resource_with_vars(request_args, obj):
    # We are doing type assertion here because, devices
    # endpoint works on per device obj level in order to
    # separate between hosts and network devices. Therefore,
    # this function is expected to work for both list of objects
    # and for a single obj.
    if isinstance(obj, list):
        r_obj = []
        for resource in obj:
            res = utils.format_variables(request_args, resource)
            r = jsonutils.to_primitive(resource, convert_instances=True)
            r['variables'] = jsonutils.to_primitive(res.vars)
            r_obj.append(r)

        return r_obj
    else:
        # This has to be a single object if not a list of objects
        res = utils.format_variables(request_args, obj)
        r = jsonutils.to_primitive(res, convert_instances=True)
        r['variables'] = jsonutils.to_primitive(res.vars)
        return r


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
        sort_keys = request_args.get('sort_keys')
        if sort_keys is not None:
            request_args['sort_keys'] = SORT_KEY_SPLITTER.split(sort_keys)
        return function(self, context, request_args=request_args,
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


def links_from(link_params):
    """Generate the list of hypermedia link relations from their parameters.

    This uses the request thread-local to determine the endpoint and generate
    URLs from that.

    :param dict link_params:
        A dictionary mapping the relation name to the query parameters.
    :returns:
        List of dictionaries to represent hypermedia link relations.
    :rtype:
        list
    """
    links = []
    relations = ["first", "prev", "self", "next"]
    base_url = flask.request.base_url

    for relation in relations:
        query_params = link_params.get(relation)
        if not query_params:
            continue
        link_rel = {
            "rel": relation,
            "href": base_url + "?" + urllib.urlencode(query_params),
        }
        links.append(link_rel)
    return links
