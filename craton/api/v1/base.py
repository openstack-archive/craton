from flask import jsonify
import flask_restful as restful

from craton.api.v1.validators import request_validate
from craton.api.v1.validators import response_filter


class Resource(restful.Resource):
    method_decorators = [request_validate, response_filter]

    def error_response(self, status_code, message):
        resp = jsonify({
            'status': status_code,
            'message': message
            })
        resp.status_code = status_code
        return resp
