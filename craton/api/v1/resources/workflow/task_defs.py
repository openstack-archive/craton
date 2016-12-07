from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton import exceptions
from craton import db as dbapi
from craton.api.v1 import base
from craton import util


LOG = log.getLogger(__name__)


class TaskDefs(base.Resource):

    @base.http_codes
    def get(self):
        """Get all available tasks to the user."""
        context = request.environ.get('context')
        tasks_obj = dbapi.taskdefs_get_all(context)
        tasks = jsonutils.to_primitive(tasks_obj)
        return [tasks], 200, None

    @base.http_codes
    def post(self):
        """Create a new task. Only users with admin context
        can create new tasks. Tasks are available to all users
        unless its restricte to a certain role by rbac."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        task_obj = dbapi.taskdefs_create(context, json)
        task = jsonutils.to_primitive(task_obj)
        return task, 200, None


class TaskDefById(base.Resource):

    @base.http_codes
    def get(self, id):
        context = request.environ.get('context')
        task_obj = dbapi.taskdefs_get_by_id(context, id)
        task = jsonutils.to_primitive(task_obj)
        return task, 200, None

    @base.http_codes
    def put(self, id):
        """Update existing task."""
        context = request.environ.get('context')
        task_obj = dbapi.taskdefs_update(context, id, request.json)
        return jsonutils.to_primitive(task_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing task."""
        context = request.environ.get('context')
        dbapi.taskdefs_delete(context, id)
        return None, 200, None
