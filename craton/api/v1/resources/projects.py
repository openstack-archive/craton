from oslo_serialization import jsonutils
from oslo_log import log

from craton.api import v1
from craton.api.v1 import base
from craton.api.v1.resources import utils
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Projects(base.Resource):

    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all projects. Requires super admin privileges."""
        project_name = request_args["name"]
        details = request_args.get("details")

        if project_name:
            projects_obj, link_params = dbapi.projects_get_by_name(
                context, project_name, request_args, pagination_params,
            )
        else:
            projects_obj, link_params = dbapi.projects_get_all(
                context, request_args, pagination_params,
            )
            if details:
                projects_obj = [utils.get_resource_with_vars(request_args, p)
                                for p in projects_obj]

        links = base.links_from(link_params)
        response_body = {'projects': projects_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    def post(self, context, request_data):
        """Create a new project. Requires super admin privileges."""
        project_obj = dbapi.projects_create(context, request_data)

        location = v1.api.url_for(
            ProjectById, id=project_obj.id, _external=True
        )
        headers = {'Location': location}

        project = jsonutils.to_primitive(project_obj)
        if 'variables' in request_data:
            project["variables"] = \
                jsonutils.to_primitive(project_obj.variables)
        else:
            project["variables"] = {}
        return project, 201, headers


class ProjectById(base.Resource):

    def get(self, context, id):
        """Get a project details by id. Requires super admin privileges."""
        project_obj = dbapi.projects_get_by_id(context, id)
        project = jsonutils.to_primitive(project_obj)
        project['variables'] = jsonutils.to_primitive(project_obj.variables)
        return project, 200, None

    def delete(self, context, id):
        """Delete existing project. Requires super admin privileges."""
        dbapi.projects_delete(context, id)
        return None, 204, None
