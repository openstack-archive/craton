from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton import exceptions
from craton import db as dbapi
from craton.api.v1 import base


LOG = log.getLogger(__name__)


class Tasks(base.Resource):

    def get(self):
        """Get all tasks available to the user."""
        context = request.environ.get('context')
        LOG.info("Get all tasks got called ...")
        try:
            tasks_obj = dbapi.tasks_get_all(context)
            LOG.info("task object is %s" % tasks_obj)
        except exceptions.NotFound:
            return [], 200, None
        except Exception as err:
            LOG.error("Error during task get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        tasks = jsonutils.to_primitive(tasks_obj)
        LOG.info("==============")
        LOG.info(tasks)
        return tasks, 200, None

    def post(self):
        """Create a new task. Only users with admin context
        can create new tasks. Tasks are available to all users
        unless its `restricte_to` a certain role."""
        context = request.environ.get('context')
        try:
            g.json["uuid"] = uuidutils.generate_uuid()
            task_obj = dbapi.task_create(context, g.json)
        except Exception as err:
            LOG.error("Error during task create: %s" % err)
            return self.error_response(500, 'Task Create Failed')

        task = jsonutils.to_primitive(task_obj)
        return task, 200, None


class TaskById(base.Resource):

    def get(self, id):
        context = request.environ.get('context')
        try:
            task_obj = dbapi.task_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during task get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        task = jsonutils.to_primitive(task_obj)
        return task, 200, None

    def put(self, id):
        """Update existing task."""
        return None, 200, None

    def delete(self, id):
        """Delete existing task."""
        context = request.environ.get('context')
        return None, 200, None
