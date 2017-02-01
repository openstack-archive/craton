from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Projects(base.Resource):

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all projects. Requires super admin privileges."""
        project_id = request_args["id"]
        project_name = request_args["name"]

        if project_id:
            project_obj = dbapi.projects_get_by_id(context, project_id)
            return jsonutils.to_primitive([project_obj], 200, None)

        if project_name:
            projects_obj = dbapi.projects_get_by_name(
                context, project_name, request_args, pagination_params,
            )
        else:
            projects_obj = dbapi.projects_get_all(
                context, request_args, pagination_params,
            )
        return jsonutils.to_primitive(projects_obj), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new project. Requires super admin privileges."""
        project_obj = dbapi.projects_create(context, request_data)
        return jsonutils.to_primitive(project_obj), 200, None


class ProjectById(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get a project details by id. Requires super admin privileges."""
        project_obj = dbapi.projects_get_by_id(context, id)
        return jsonutils.to_primitive(project_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing project. Requires super admin privileges."""
        dbapi.projects_delete(context, id)
        return None, 204, None


class ProjectsVariables(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get variables for given project. Requires super admin privileges."""
        obj = dbapi.projects_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, context, id, request_data):
        """
        Update existing project variables, or create if it does
        not exist. Requires super admin privileges.
        """
        obj = dbapi.projects_variables_update(context, id, request_data)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, context, id, request_data):
        """Delete project variables. Requires super admin privileges."""
        dbapi.projects_variables_delete(context, id, request_data)
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        return None, 204, None
