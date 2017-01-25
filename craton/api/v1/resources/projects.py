from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Projects(base.Resource):

    @base.http_codes
    def get(self, context, request_args):
        """Get all projects. Requires super admin privileges."""
        project_id = request_args["id"]
        project_name = request_args["name"]

        if project_name:
            project_obj = dbapi.projects_get_by_name(context, project_name)
            return jsonutils.to_primitive([project_obj]), 200, None

        if project_id:
            project_obj = dbapi.projects_get_by_id(context, project_id)
            return jsonutils.to_primitive([project_obj], 200, None)

        projects_obj = dbapi.projects_get_all(context)
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
    def put(self, context, id, request_data):
        """Update existing Project."""
        project_obj = dbapi.projects_update(context, id, request_data)
        return jsonutils.to_primitive(project_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing project. Requires super admin privileges."""
        dbapi.projects_delete(context, id)
        return None, 204, None
