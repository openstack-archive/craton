import contextlib
from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_utils import uuidutils
from taskflow.persistence import models
from taskflow import engines
from stevedore import driver

from craton import exceptions
from craton import db as dbapi
from craton.api.v1 import base

from craton.workflow import worker


LOG = log.getLogger(__name__)


def workflow_factory(name, *args, **kwargs):
    mgr = driver.DriverManager(
        namespace='craton.workflow', name=name,
        invoke_on_load=True, invoke_args=args, invoke_kwds=kwargs)
    return mgr.driver.workflow()

def make_save_book(persistence, job_id, flow_plugin,
                   plugin_args=(), plugin_kwds={}):
    flow_id = book_id = job_id  # Do these need to be different?
    book = models.LogBook(book_id)
    detail = models.FlowDetail(flow_id, uuidutils.generate_uuid())
    book.add(detail)

    factory_args = [flow_plugin] + list(plugin_args)
    factory_kwargs = plugin_kwds
    engines.save_factory_details(detail, workflow_factory,
                                 factory_args, factory_kwargs)
    with contextlib.closing(persistence.get_connection()) as conn:
        conn.save_logbook(book)
        return book


class Jobs(base.Resource):

    def get(self):
        """Get all jobs by the user."""
        context = request.environ.get('context')
        try:
            jobs_obj = dbapi.jobs_get_all(context)
        except exceptions.NotFound:
            return [], 200, None
        except Exception as err:
            LOG.error("Error during workflow get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        jobs = jsonutils.to_primitive(jobs_obj)
        return jobs, 200, None

    def post(self):
        """Create a new jobs."""
        context = request.environ.get('context')
        LOG.info(g.json)
        workflow_uuid = g.json.get("workflow_uuid")
        user_vars = g.json.get("vars", {})

        if not workflow_uuid:
            return self.error_response(400, "workflow (uuid) is needed")

        try:
            wf = dbapi.get_workflow_by_uuid(context, workflow_uuid)
            LOG.info("Found workflow %s" % wf.uuid)
        except exceptions.NotFound:
            return self.error_response(404,
                                  "Workflow %s not found" % workflow)

        try:
            persistence = worker.get_persistence_backend()
            job_uuid = uuidutils.generate_uuid()
            book = make_save_book(persistence, job_uuid, wf.name,
                                  plugin_kwds=dict(user_vars))

            board = worker.get_jobboard_backend()
            board.connect()
            LOG.debug("Posting job %s" % book.uuid)
            details = {}
            board.post(job_uuid, book=book,details=details)

            g.json["uuid"] = book.uuid
            job_obj = dbapi.jobs_create(context, g.json)

        except Exception as err:
            LOG.error("Error during workflow create: %s" % err)
            return self.error_response(500, 'Workflow Create Failed')

        job = jsonutils.to_primitive(job_obj)
        return job, 200, None
