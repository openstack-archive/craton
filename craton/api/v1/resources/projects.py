from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Projects(base.Resource):

    @base.http_codes
    def get(self):
        """Get all projects. Requires super admin privileges."""
        project_id = g.args["id"]
        project_name = g.args["name"]
        context = request.environ.get('context')

        if project_name:
            project_obj = dbapi.projects_get_by_name(context, project_name)
            return jsonutils.to_primitive([project_obj]), 200, None

        if project_id:
            project_obj = dbapi.projects_get_by_id(context, project_id)
            return jsonutils.to_primitive([project_obj], 200, None)

        projects_obj = dbapi.projects_get_all(context)
        return jsonutils.to_primitive(projects_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new project. Requires super admin privileges."""
        context = request.environ.get('context')
        project_obj = dbapi.projects_create(context, g.json)
        return jsonutils.to_primitive(project_obj), 200, None


class ProjectById(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get a project details by id. Requires super admin privileges."""
        context = request.environ.get('context')
        project_obj = dbapi.projects_get_by_id(context, id)
        return jsonutils.to_primitive(project_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing project. Requires super admin privileges."""
        context = request.environ.get('context')
        dbapi.projects_delete(context, id)
        return None, 204, None
