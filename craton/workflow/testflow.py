import time

from oslo_log import log as logging
from taskflow import task
from taskflow.patterns import linear_flow

from craton.workflow import base

LOG = logging.getLogger(__name__)


class Sleep(task.Task):
    def __init__(self, delay=10, **kwargs):
        super(Sleep, self).__init__(**kwargs)
        self.delay = delay

    def execute(self):
        LOG.info('Doing task %s', self)
        time.sleep(self.delay)


class Fail(task.Task):
    def execute(self):
        LOG.info('Failing task %s', self)
        raise RuntimeError('failure in task %s' % self)


class TestFlow(base.WorkflowFactory):
    def __init__(self, task_delay=5):
        super(TestFlow, self).__init__()
        self.task_delay = task_delay

    def workflow(self):
        f = linear_flow.Flow('example')
        f.add(
            Sleep(name='step 1', delay=self.task_delay),
            Sleep(name='step 2', delay=self.task_delay),
            Fail(name='step 3'),
        )
        return f
