import contextlib
import threading

from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import uuidutils
from taskflow.conductors import backends as conductors
from taskflow.jobs import backends as boards
from taskflow.persistence import backends as persistence_backends
from zake import fake_client


LOG = logging.getLogger(__name__)
CONF = cfg.CONF

OPTS = [
    cfg.StrOpt('job_board_name', default='craton_jobs',
               help='Name of job board used to store outstanding jobs.'),
    cfg.IntOpt('max_simultaneous_jobs', default=9,
               help='Number of tasks to run in parallel on this worker.'),
]
CONF.register_opts(OPTS)

TASKFLOW_OPTS = [
    cfg.StrOpt('connection', default='memory',
               help='Taskflow backend used for persisting taskstate.'),
    cfg.StrOpt('job_board_url',
               default='zookeeper://localhost?path=/taskflow/craton/jobs',
               help='URL used to store outstanding jobs'),
    cfg.BoolOpt('db_upgrade', default=True,
                help='Upgrade DB schema on startup.'),
]
CONF.register_opts(TASKFLOW_OPTS, group='taskflow')


def _get_persistence_backend(conf):
    return persistence_backends.fetch({
        'connection': conf.taskflow.connection,
    })


def _get_jobboard_backend(conf, persistence=None):
    client = None
    if conf.taskflow.connection == 'memory':
        client = fake_client.FakeClient()
    return boards.fetch(conf.job_board_name,
                        {'board': conf.taskflow.job_board_url},
                        client=client, persistence=persistence)


def start(conf):
    persistence = _get_persistence_backend(conf)

    if conf.taskflow.db_upgrade:
        with contextlib.closing(persistence.get_connection()) as conn:
            LOG.info('Checking for database schema upgrade')
            conn.upgrade()

    my_name = uuidutils.generate_uuid()
    LOG.info('I am %s', my_name)

    board = _get_jobboard_backend(conf, persistence=persistence)

    conductor = conductors.fetch(
        'nonblocking', my_name, board,
        engine='parallel',
        max_simultaneous_jobs=conf.max_simultaneous_jobs,
        persistence=persistence)

    board.connect()
    LOG.debug('Starting taskflow conductor loop')
    threading.Thread(target=conductor.run).start()

    return persistence, board, conductor
