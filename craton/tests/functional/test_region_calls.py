from craton.tests.functional import TestCase

from cratonclient import session
from cratonclient.v1 import client
from cratonclient.v1 import regions


class APIV1RegionTest(TestCase):

    def setUp(self):
        super(APIV1RegionTest, self).setUp()
        self.username = 'demo'
        self.token = 'demo'
        self.project_id = 'b9f10eca66ac4c279c139d01e65f96b4'
        self.service_ip = self.container_data['NetworkSettings']['IPAddress']
        self.url = 'http://{}:8080/'.format(self.service_ip)
        self.session = session.Session(username=self.username,
                                       token=self.token,
                                       project_id=self.project_id)
        self.client = client.Client(session=self.session,
                                    url=self.url)

    def test_regions_get_all(self):
        r = regions.RegionManager(self.session, self.url)
        rlist = r.list()
        self.assertEqual(rlist, {})
