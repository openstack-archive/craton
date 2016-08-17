from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Projects(base.Resource):

    def get(self):
        """Get all the project. This is admin only function.
        """
        project_id = g.args["id"]
        project_name = g.args["name"]
        context = request.environ.get('context')

        if not project_id and not project_name:
            try:
                projects_obj = dbapi.projects_get_all(context)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if projects_obj:
                result = jsonutils.to_primitive(projects_obj)
                return result, 200, None
            else:
                return None, 404, None

        if project_name:
            try:
                project_obj = dbapi.projects_get_by_name(context, project_name)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if project_obj:
                result = jsonutils.to_primitive(project_obj)
                return [result], 200, None
            else:
                return None, 404, None

        # Project Ids are unique
        if project_id:
            try:
                project_obj = dbapi.projects_get_by_id(context, project_id)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if project_obj:
                project_obj.data = project_obj.variables
                result = jsonutils.to_primitive(project_obj)
                return [result], 200, None
            else:
                return None, 404, None

    def post(self):
        """Create a new project. This is admin only function."""
        context = request.environ.get('context')
        try:
            project_obj = dbapi.projects_create(context, g.json)
        except Exception as err:
            LOG.error("Error during project create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        project = jsonutils.to_primitive(project_obj)
        return project, 200, None


class ProjectById(base.Resource):

    def get(self, id):
        """Get a project details by id."""
        context = request.environ.get('context')
        try:
            project_obj = dbapi.proejcts_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during Project get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        project_obj.data = project_obj.variables
        project = jsonutils.to_primitive(project_obj)
        return project, 200, None

    def put(self, id):
        """Update existing project."""
        return None, 200, None

    def delete(self, id):
        """Delete existing project."""
        context = request.environ.get('context')
        try:
            dbapi.projects_delete(context, id)
        except Exception as err:
            LOG.error("Error during project delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None


class ProjectData(base.Resource):

    def put(self, id):
        """
        Update existing project data, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        try:
            dbapi.projects_data_update(context, id, request.json)
        except Exception as err:
            LOG.error("Error during project data update: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None

    def delete(self, id):
        """Delete project data."""
        context = request.environ.get('context')
        try:
            dbapi.projects_data_delete(context, id, request.json)
        except Exception as err:
            LOG.error("Error during projects data delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None
