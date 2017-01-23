# The code is auto generated, your change will be overwritten by
# code generating.

from datetime import date
from functools import wraps

from werkzeug.datastructures import MultiDict, Headers
from flask import request, current_app, json
from flask_restful import abort
from flask_restful.utils import unpack
from jsonschema import Draft4Validator
from oslo_log import log

from craton.api.v1.schemas import filters
from craton.api.v1.schemas import scopes
from craton.api.v1.schemas import validators
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func


security = Security()


def merge_default(schema, value):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    return normalize(schema, value, type_defaults)[0]


def normalize(schema, data, required_defaults=None):

    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            if hasattr(self.data, key):
                return getattr(self.data, key)
            else:
                return default

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return self.data.keys()
            return vars(self.data).keys()

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for pattern, _schema in (schema.get('patternProperties', {})).items():
            if pattern == "^.+":
                for key in data.keys():
                    result[key] = _normalize(_schema, data.get(key))

        for key, _schema in schema.get('properties', {}).items():
            # set default
            type_ = _schema.get('type', 'object')
            if ('default' not in _schema and
                key in schema.get('required', []) and
                    type_ in required_defaults):
                _schema['default'] = required_defaults[type_]

            # get value
            if data.has(key):
                result[key] = _normalize(_schema, data.get(key))
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                errors.append(dict(name='property_missing',
                                   message='`%s` is required' % key))

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            rs_component.update(result)
            result = rs_component

        if schema.get('anyOf'):
            # In case of anyOf simply return data, since we dont
            # care in normalization of the data as long as
            # its been verified.
            result = data.data

        additional_properties_schema = schema.get('additionalProperties',
                                                  False)
        if additional_properties_schema:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema,
                                         data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, dict):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize(schema, data):
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if type_ not in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class FlaskValidatorAdaptor(object):

    def __init__(self, schema):
        self.validator = Draft4Validator(schema)

    def type_convert(self, obj):
        if obj is None:
            return None
        if isinstance(obj, (dict, list)) and not isinstance(obj, MultiDict):
            return obj
        if isinstance(obj, Headers):
            obj = MultiDict(obj)
        result = dict()

        convert_funs = {
            'integer': lambda v: int(v[0]),
            'boolean': lambda v: v[0].lower() not in ['n', 'no',
                                                      'false', '', '0'],
            'null': lambda v: None,
            'number': lambda v: float(v[0]),
            'string': lambda v: v[0]
        }

        def convert_array(type_, v):
            func = convert_funs.get(type_, lambda v: v[0])
            return [func([i]) for i in v]

        for k, values in obj.lists():
            prop = self.validator.schema['properties'].get(k, {})
            type_ = prop.get('type')
            fun = convert_funs.get(type_, lambda v: v[0])
            if type_ == 'array':
                item_type = prop.get('items', {}).get('type')
                result[k] = convert_array(item_type, values)
            else:
                result[k] = fun(values)
        return result

    def validate(self, value):
        value = self.type_convert(value)
        errors = list(e.message for e in self.validator.iter_errors(value))
        if errors:
            abort(422, message='Unprocessable Entity', errors=errors)
        return merge_default(self.validator.schema, value)


def request_validate(view):

    @wraps(view)
    def wrapper(*args, **kwargs):
        endpoint = request.endpoint.partition('.')[-1]
        # scope
        if (endpoint, request.method) in scopes and not set(
                scopes[(endpoint,
                        request.method)]).issubset(set(security.scopes)):
            abort(403)
        # data
        method = request.method
        if method == 'HEAD':
            method = 'GET'
        locations = validators.get((endpoint, method), {})
        data_type = {"json": "request_data", "args": "request_args"}
        for location, schema in locations.items():
            value = getattr(request, location, MultiDict())
            validator = FlaskValidatorAdaptor(schema)
            result = validator.validate(value)
            kwargs[data_type[location]] = result
            LOG.info("Validated request %s: %s" % (location, result))
        context = request.environ['context']
        return view(*args, context=context, **kwargs)

    return wrapper


def ensure_project_exists(view):

    @wraps(view)
    def wrapper(*args, **kwargs):
        context = request.environ['context']
        if context.using_keystone:
            find_or_create_project(request, context)
        return view(*args, **kwargs)

    return wrapper


def response_filter(view):

    @wraps(view)
    def wrapper(*args, **kwargs):
        resp = view(*args, **kwargs)

        if isinstance(resp, current_app.response_class):
            return resp

        endpoint = request.endpoint.partition('.')[-1]
        method = request.method
        if method == 'HEAD':
            method = 'GET'
        try:
            resp_filter = filters[(endpoint, method)]
        except KeyError:
            LOG.error(
                '"(%(endpoint)s, %(method)s)" is not defined in the response '
                'filters.',
                {"endpoint": endpoint, "method": method}
            )
            abort(500)

        headers = None
        status = None
        if isinstance(resp, tuple):
            resp, status, headers = unpack(resp)

        try:
            schemas = resp_filter[status]
        except KeyError:
            LOG.error(
                'The status code %(status)d is not defined in the response '
                'filter "(%(endpoint)s, %(method)s)".',
                {"status": status, "endpoint": endpoint, "method": method}
            )
            abort(500)

        resp, errors = normalize(schemas['schema'], resp)
        if schemas['headers']:
            headers, header_errors = normalize(
                {'properties': schemas['headers']}, headers)
            errors.extend(header_errors)
        if errors:
            abort(500, message='Expectation Failed', errors=errors)

        return current_app.response_class(
            json.dumps(resp, cls=JSONEncoder) + '\n',
            status=status,
            headers=headers,
            mimetype='application/json'
        )

    return wrapper


def find_or_create_project(request, context):
    project_id = context.tenant
    token_info = context.token_info
    try:
        dbapi.projects_get_by_id(context, project_id)
    except exceptions.NotFound:
        LOG.info('Adding Project "%s" to projects table', project_id)
        dbapi.projects_create(context,
                              {'id': project_id,
                               'name': token_info['project']['name']})
