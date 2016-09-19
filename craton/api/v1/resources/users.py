from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton.api.v1 import base
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Users(base.Resource):

    def get(self):
        """Get all users. Requires project admin privileges."""
        user_id = g.args["id"]
        user_name = g.args["name"]
        context = request.environ.get('context')

        if not user_id and not user_name:
            try:
                users_obj = dbapi.users_get_all(context)
            except exceptions.AdminRequired:
                return self.error_response(401, 'This is admin only resource.')

            if users_obj:
                result = jsonutils.to_primitive(users_obj)
                return result, 200, None
            else:
                return None, 404, None

        if user_name:
            try:
                users_obj = dbapi.users_get_by_name(context, user_name)
            except exceptions.AdminRequired:
                return self.error_response(401, 'This is admin only resource.')

            if users_obj:
                result = jsonutils.to_primitive(users_obj)
                return [result], 200, None
            else:
                return None, 404, None

        # User Ids are unique
        if user_id:
            try:
                user_obj = dbapi.users_get_by_id(context, user_id)
            except exceptions.AdminRequired:
                return self.error_response(401, 'This is admin only resource.')
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if user_obj:
                user_obj.data = user_obj.variables
                result = jsonutils.to_primitive(user_obj)
                return [result], 200, None
            else:
                return None, 404, None

    def post(self):
        """Create a new user. Requires project admin privileges."""
        context = request.environ.get('context')

        try:
            project_id = g.json["project"]
            dbapi.projects_get_by_id(context, project_id)
        except exceptions.NotFound:
            return self.error_response(404, 'Project with given id not found')

        try:
            api_key = uuidutils.generate_uuid()
            g.json["api_key"] = api_key
            user_obj = dbapi.users_create(context, g.json)
        except exceptions.AdminRequired:
            return self.error_response(401, 'This is admin only resource.')
        except Exception as err:
            LOG.error("Error during user create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        user = jsonutils.to_primitive(user_obj)
        return user, 200, None


class UserById(base.Resource):

    def get(self, id):
        """Get a user details by id. Requires project admin privileges."""
        context = request.environ.get('context')
        try:
            user_obj = dbapi.users_get_by_id(context, id)
        except exceptions.AdminRequired:
            return self.error_response(401, 'This is admin only resource.')
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during User get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        user = jsonutils.to_primitive(user_obj)
        return user, 200, None

    def put(self, id):
        """Update existing user. Requires project admin privileges."""
        return None, 200, None

    def delete(self, id):
        """Delete existing user. Requires project admin privileges."""
        context = request.environ.get('context')
        try:
            dbapi.users_delete(context, id)
        except exceptions.AdminRequired:
            return self.error_response(401, 'This is admin only resource.')
        except Exception as err:
            LOG.error("Error during user delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None
