from flask import g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Users(base.Resource):

    @base.http_codes
    def get(self, context):
        """Get all users. Requires project admin privileges."""
        user_id = g.args["id"]
        user_name = g.args["name"]

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
    def post(self, context):
        """Create a new user. Requires project admin privileges."""
        json = util.copy_project_id_into_json(context, g.json)
        project_id = json["project_id"]
        dbapi.projects_get_by_id(context, project_id)
        api_key = uuidutils.generate_uuid()
        g.json["api_key"] = api_key
        user_obj = dbapi.users_create(context, json)
        return jsonutils.to_primitive(user_obj), 200, None


class UserById(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get a user details by id. Requires project admin privileges."""
        user_obj = dbapi.users_get_by_id(context, id)
        return jsonutils.to_primitive(user_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing user. Requires project admin privileges."""
        dbapi.users_delete(context, id)
        return None, 204, None
