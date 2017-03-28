from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton.api import v1
from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Users(base.Resource):

    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all users. Requires project admin privileges."""
        user_id = request_args["id"]
        user_name = request_args["name"]

        if user_id:
            user_obj = dbapi.users_get_by_id(context, user_id)
            user_obj.data = user_obj.variables
            users_obj = [user_obj]
            link_params = {}

        if user_name:
            users_obj, link_params = dbapi.users_get_by_name(
                context, user_name, request_args, pagination_params,
            )
        else:
            users_obj, link_params = dbapi.users_get_all(
                context, request_args, pagination_params,
            )
        links = base.links_from(link_params)
        response_body = {'users': users_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    def post(self, context, request_data):
        """Create a new user. Requires project admin privileges."""
        # NOTE(sulo): Instead of using context project_id from
        # header, here we always ensure, user create gets project_id
        # from request param.
        project_id = request_data["project_id"]
        dbapi.projects_get_by_id(context, project_id)
        api_key = uuidutils.generate_uuid()
        request_data["api_key"] = api_key
        user_obj = dbapi.users_create(context, request_data)

        location = v1.api.url_for(
            UserById, id=user_obj.id, _external=True
        )
        headers = {'Location': location}

        return jsonutils.to_primitive(user_obj), 201, headers


class UserById(base.Resource):

    def get(self, context, id):
        """Get a user details by id. Requires project admin privileges."""
        user_obj = dbapi.users_get_by_id(context, id)
        return jsonutils.to_primitive(user_obj), 200, None

    def delete(self, context, id):
        """Delete existing user. Requires project admin privileges."""
        dbapi.users_delete(context, id)
        return None, 204, None
