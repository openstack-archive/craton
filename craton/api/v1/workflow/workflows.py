from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton import exceptions
from craton import db as dbapi
from craton.api.v1 import base


LOG = log.getLogger(__name__)


class Workflows(base.Resource):

    def get(self):
        """Get all workflows available to the user."""
        context = request.environ.get('context')
        try:
            wf_obj = dbapi.workflows_get_all(context)
        except exceptions.NotFound:
            return [], 200, None
        except Exception as err:
            LOG.error("Error during workflow get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        wf = jsonutils.to_primitive(wf_obj)
        return wf, 200, None

    def post(self):
        """Create a new workflows."""
        context = request.environ.get('context')
        try:
            g.json["uuid"] = uuidutils.generate_uuid()
            LOG.info("Creating workflow %s" % g.json)
            wf_obj = dbapi.workflow_create(context, g.json)
        except Exception as err:
            LOG.error("Error during workflow create: %s" % err)
            return self.error_response(500, 'Workflow Create Failed')

        wf = jsonutils.to_primitive(wf_obj)
        return wf, 200, None


class WorkflowById(base.Resource):

    def get(self, id):
        """Get workflow by id."""
        context = request.environ.get('context')
        return None, 200, None

    def put(self, id):
        """Update existing workflow."""
        return None, 200, None

    def delete(self, id):
        """Delete existing workflow."""
        context = request.environ.get('context')
        return None, 200, None
