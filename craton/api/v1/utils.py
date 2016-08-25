from flask import g
from flask import request

from craton.api.v1.schemas import validators


def extract_variable_filters():
    """Extract variable filters. Filters can be defined as part of the
    schema. Such filter keys are reserved, however, users can pass in
    any key, value pair for variable filtering.
    """
    endpoint = request.endpoint.partition('.')[-1]
    method = request.method
    locations = validators.get((endpoint, method), {})

    reserved_args = [arg for arg in locations['args']['properties'].keys()]

    vars_filters = {}
    for key, value in g.args.items():
        if key not in reserved_args:
            vars_filters[key] = value

    return vars_filters
