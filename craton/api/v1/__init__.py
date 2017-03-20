from flask import Blueprint
import flask_restful as restful

from craton.api.v1.routes import routes
from craton.util import handle_all_exceptions


class CratonApi(restful.Api):

    def error_router(self, _, e):
        return self.handle_error(e)

    def handle_error(self, e):
        return handle_all_exceptions(e)


bp = Blueprint('v1', __name__)
api = CratonApi(bp, catch_all_404s=False)

for route in routes:
    api.add_resource(route.pop('resource'), *route.pop('urls'), **route)
