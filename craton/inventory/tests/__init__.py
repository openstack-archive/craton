import mock
import testtools
from oslo_middleware import base


class TestContext(base.Middleware):
    def __init__(self, auth_token=None, user=None, tenant=None,
                 is_admin=False):
        self.auth_token = auth_token
        self.user = user
        self.tenant = tenant
        self.is_admin = is_admin


def make_context(*args, **kwargs):
    return TestContext(*args, **kwargs)


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.addCleanup(mock.patch.stopall)

        self.context = make_context(auth_token='fake-token',
                                    user='fake-user',
                                    tenant='fake-tenant',
                                    is_admin=True)
