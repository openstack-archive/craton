from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton import exceptions
from craton import db as dbapi
from craton.api.v1 import base
from craton import util


LOG = log.getLogger(__name__)


class WorkflowDefs(base.Resource):

    @base.http_codes
    def get(self):
        """Get all available workflow definition to the user."""
        context = request.environ.get('context')
        workflow_obj = dbapi.workflow_defs_get_all(context)
        workflows = jsonutils.to_primitive(workflow_obj)
        return [workflows], 200, None

    @base.http_codes
    def post(self):
        """Create a new workflow."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        workflow_obj = dbapi.workflow_defs_create(context, json)
        workflow = jsonutils.to_primitive(workflow_obj)
        return workflow, 200, None


class WorkflowDefById(base.Resource):

    @base.http_codes
    def get(self, id):
        context = request.environ.get('context')
        workflow_obj = dbapi.workflow_defs_get_by_id(context, id)
        workflow = jsonutils.to_primitive(workflow_obj)
        return workflow, 200, None

    @base.http_codes
    def put(self, id):
        """Update existing workflow."""
        context = request.environ.get('context')
        workflow_obj = dbapi.workflow_defs_update(context, id, request.json)
        return jsonutils.to_primitive(workflow_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing workflow."""
        context = request.environ.get('context')
        dbapi.workflowdefs_delete(context, id)
        return None, 200, None
