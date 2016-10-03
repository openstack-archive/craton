from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Users(base.Resource):

    @base.http_codes
    def get(self):
        """Get all users. Requires project admin privileges."""
        user_id = g.args["id"]
        user_name = g.args["name"]
        context = request.environ.get('context')

        if user_name:
            user_obj = dbapi.users_get_by_name(context, user_name)
            user_obj.data = user_obj.variables
            return jsonutils.to_primitive([user_obj]), 200, None

        if user_id:
            user_obj = dbapi.users_get_by_id(context, user_id)
            user_obj.data = user_obj.variables
            return jsonutils.to_primitive([user_obj]), 200, None

        users_obj = dbapi.users_get_all(context)
        return jsonutils.to_primitive(users_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new user. Requires project admin privileges."""
        context = request.environ.get('context')
        project_id = g.json["project_id"]
        dbapi.projects_get_by_id(context, project_id)
        api_key = uuidutils.generate_uuid()
        g.json["api_key"] = api_key
        user_obj = dbapi.users_create(context, g.json)
        return jsonutils.to_primitive(user_obj), 200, None


class UserById(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get a user details by id. Requires project admin privileges."""
        context = request.environ.get('context')
        user_obj = dbapi.users_get_by_id(context, id)
        return jsonutils.to_primitive(user_obj), 200, None

    def put(self, id):
        """Update existing user. Requires project admin privileges."""
        return None, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing user. Requires project admin privileges."""
        context = request.environ.get('context')
        dbapi.users_delete(context, id)
        return None, 204, None
