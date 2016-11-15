from craton.tests.functional import TestCase

from cratonclient import session
from cratonclient.v1 import client


class APIV1CellTest(TestCase):

    def setUp(self):
        super(APIV1CellTest, self).setUp()
        if self.container_setup_error:
            self.skipTest('Error setting up service container')
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

    def test_cells_get_all(self):
        inventory = self.client.inventory(1)
        cells = inventory.cells.list()
        self.assertEqual(cells, [])
