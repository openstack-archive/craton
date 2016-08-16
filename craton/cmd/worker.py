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

    conductor.wait()
    sys.exit(0)


if __name__ == '__main__':
    main()
