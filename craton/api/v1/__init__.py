from flask import Blueprint
import flask_restful as restful

from craton.api.v1.routes import routes
from craton.api.v1.validators import security


@security.scopes_loader
def current_scopes():
    return []


bp = Blueprint('v1', __name__)
api = restful.Api(bp, catch_all_404s=True)

for route in routes:
    api.add_resource(route.pop('resource'), *route.pop('urls'), **route)
