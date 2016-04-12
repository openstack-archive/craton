import flask_restful as restful
from craton.inventory.api.v1.validators import request_validate, response_filter


class Resource(restful.Resource):
    method_decorators = [request_validate, response_filter]
