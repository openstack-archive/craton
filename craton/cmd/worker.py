import contextlib
import signal
import sys

from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import uuidutils
from stevedore import driver
from taskflow import engines
from taskflow.persistence import models

from craton.workflow import worker

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


# This needs to be a globally accessible (ie: top-level) function, so
# flow recovery can execute it to re-create the intended workflows.
def workflow_factory(name, *args, **kwargs):
    mgr = driver.DriverManager(
        namespace='craton.workflow', name=name,
        invoke_on_load=True, invoke_args=args, invoke_kwds=kwargs)
    return mgr.driver.workflow()


def main():
    logging.register_options(CONF)
    CONF(sys.argv[1:], project='craton-worker', default_config_files=[])
    logging.setup(CONF, 'craton')

    persistence, board, conductor = worker.start(CONF)

    def stop(signum, _frame):
        LOG.info('Caught signal %s, gracefully exiting', signum)
        conductor.stop()
    signal.signal(signal.SIGTERM, stop)

    # TODO(gus): eventually feeding in jobs will happen elsewhere and
    # main() will end here.
    #
    # conductor.wait()
    # sys.exit(0)

    def make_save_book(persistence, job_id,
                       flow_plugin, plugin_args=(), plugin_kwds={}):
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

    # Feed in example task
    job_uuid = uuidutils.generate_uuid()
    LOG.debug('Posting job %s', job_uuid)
    details = {
        'store': {
            'foo': 'bar',
        },
    }

    job = board.post(
        job_uuid,
        book=make_save_book(
            persistence, job_uuid,
            'testflow', plugin_kwds=dict(task_delay=2)),
        details=details)

    # Run forever.  TODO(gus): This is what we want to do in production
    # conductor.wait()
    job.wait()
    LOG.debug('Job finished: %s', job.state)
    conductor.stop()


if __name__ == '__main__':
    main()
