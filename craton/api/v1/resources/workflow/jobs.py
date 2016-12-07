from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils

from craton import exceptions
from craton import db as dbapi
from craton.api.v1 import base

from craton.workflow import worker


LOG = log.getLogger(__name__)


class Jobs(base.Resource):

    @base.http_codes
    def get(self):
        """Get all jobs by the user."""
        context = request.environ.get('context')
        jobs_obj = dbapi.workflows_get_all(context)
        jobs = jsonutils.to_primitive(jobs_obj)
        return jobs, 200, None

    @base.http_codes
    def post(self):
        """Create a new job for execution."""
        context = request.environ.get('context')

        workflow_def_id = g.json.get("workflow_def_id")
        try:
            wf_def = dbapi.get_workflow_def_by_id(context, workflow_def_id)
        except exceptions.NotFound:
            return self.error_response(404,
                                  "Workflow %s not found" % workflow)

        job_obj = dbapi.jobs_create(context, g.json)
        job = jsonutils.to_primitive(job_obj)
        return job, 200, None
