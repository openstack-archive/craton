import mock

from oslo_serialization import jsonutils

from craton.inventory import api
from craton.inventory import exceptions
from craton.inventory.api import middleware
from craton.inventory.db.sqlalchemy import api as dbapi
from craton.inventory.tests import TestCase
from craton.inventory.tests.unit import fake_resources


class APIV1Test(TestCase):
    def setUp(self):
        super(APIV1Test, self).setUp()

        # Create the app first
        self.app = api.setup_app()
        # Put the context middleware
        self.app.wsgi_app = middleware.NoAuthContextMiddleware(
            self.app.wsgi_app)
        # Create client
        self.client = self.app.test_client()

    def get(self, path, **kw):
        resp = self.client.get(path=path)
        resp.json = jsonutils.loads(resp.data.decode('utf-8'))
        return resp

    def post(self, path, data, **kw):
        content = jsonutils.dumps(data)
        content_type = 'application/json'
        resp = self.client.post(path=path, content_type=content_type,
                                data=content)
        resp.json = jsonutils.loads(resp.data.decode('utf-8'))
        return resp

    def delete(self, path):
        resp = self.client.delete(path=path)
        return resp


class APIV1CellsIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'cells_get_by_id')
    def test_get_cells_by_id(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL1
        resp = self.get('v1/cells/1')
        self.assertEqual(resp.json["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_by_id')
    def test_get_cells_by_bad_id_is_404(self, mock_cells):
        mock_cells.side_effect = exceptions.NotFound()
        resp = self.get('v1/cells/3')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'cells_delete')
    def test_cells_delete(self, mock_cell):
        resp = self.delete('v1/cells/1')
        self.assertEqual(200, resp.status_code)


class APIV1CellsTest(APIV1Test):
    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL_LIST
        resp = self.get('v1/cells')
        self.assertEqual(len(resp.json), len(fake_resources.CELL_LIST))

    @mock.patch.object(dbapi, 'cells_get_by_name')
    def test_get_cells_with_name_filters(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL1
        resp = self.get('v1/cells?region=1&name=cell1')
        self.assertEqual(len(resp.json), 1)
        # Ensure we got the right cell
        self.assertEqual(resp.json[0]["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_by_id')
    def test_get_cells_with_id_filters(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL1
        resp = self.get('v1/cells?region=1&id=1')
        self.assertEqual(len(resp.json), 1)
        # Ensure we got the right cell
        self.assertEqual(resp.json[0]["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_by_name')
    def test_get_cell_no_exist_by_name_fails(self, mock_cell):
        err = exceptions.NotFound()
        mock_cell.side_effect = err
        resp = self.get('v1/cells?region=1&name=dontexist')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_with_valid_data(self, mock_cell):
        mock_cell.return_value = None
        data = {'name': 'cell1', 'region_id': 1, 'project_id': "1"}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_returns_cell_obj(self, mock_cell):
        return_value = {'name': 'cell1', 'region_id': 1,
                        'project_id': 1, 'id': 1}
        mock_cell.return_value = return_value
        data = {'name': 'cell1', 'region_id': 1, 'project_id': "1"}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(return_value, resp.json)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_fails_with_invalid_data(self, mock_cell):
        mock_cell.return_value = None
        # data is missing required cell name
        data = {'region_id': 1, 'project_id': "1"}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(422, resp.status_code)


class APIV1RegionsIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'regions_get_by_id')
    def test_regions_get_by_id(self, mock_regions):
        mock_regions.return_value = fake_resources.REGION1
        resp = self.get('v1/regions/1')
        self.assertEqual(resp.json["name"], fake_resources.REGION1.name)

    @mock.patch.object(dbapi, 'regions_get_by_id')
    def test_regions_get_by_bad_id_is_404(self, mock_regions):
        mock_regions.side_effect = exceptions.NotFound()
        resp = self.get('v1/regions/1')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'regions_delete')
    def test_delete_region(self, mock_region):
        resp = self.delete('v1/regions/1')
        self.assertEqual(200, resp.status_code)


class APIV1RegionsTest(APIV1Test):
    @mock.patch.object(dbapi, 'regions_get_all')
    def test_regions_get_all(self, mock_regions):
        mock_regions.return_value = fake_resources.REGIONS_LIST
        resp = self.get('v1/regions')
        self.assertEqual(len(resp.json), len(fake_resources.REGIONS_LIST))

    @mock.patch.object(dbapi, 'regions_get_by_name')
    def test_regions_get_by_name_filters(self, mock_regions):
        mock_regions.return_value = fake_resources.REGION1
        resp = self.get('v1/regions?name=region1')
        self.assertEqual(resp.json[0]["name"], fake_resources.REGION1.name)

    @mock.patch.object(dbapi, 'regions_get_by_id')
    def test_regions_get_by_id_filters(self, mock_regions):
        mock_regions.return_value = fake_resources.REGION1
        resp = self.get('v1/regions?id=1')
        self.assertEqual(resp.json[0]["name"], fake_resources.REGION1.name)

    @mock.patch.object(dbapi, 'regions_get_by_name')
    def test_get_region_no_exist_by_name_fails(self, mock_regions):
        mock_regions.side_effect = exceptions.NotFound()
        resp = self.get('v1/regions?name=bla')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'regions_create')
    def test_post_region_with_valid_data(self, mock_region):
        mock_region.return_value = None
        data = {'name': 'region1', 'project_id': '1'}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'regions_create')
    def test_create_region_returns_region_obj(self, mock_region):
        return_value = {'name': 'region1', 'project_id': '1', 'id': 1}
        mock_region.return_value = return_value
        data = {'name': 'region1', 'project_id': '1'}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(return_value, resp.json)

    @mock.patch.object(dbapi, 'regions_create')
    def test_post_region_with_invalid_data_fails(self, mock_region):
        mock_region.return_value = None
        data = {'project_id': '1'}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(422, resp.status_code)


class APIV1HostsIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_by_id(self, mock_hosts):
        mock_hosts.return_value = fake_resources.HOST1
        resp = self.get('v1/hosts/1')
        self.assertEqual(resp.json["name"], fake_resources.HOST1.name)

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_by_bad_id_is_404(self, mock_hosts):
        mock_hosts.side_effect = exceptions.NotFound()
        resp = self.get('v1/hosts/1')
        self.assertEqual(404, resp.status_code)


class APIV1HostsTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_hosts_by_region_gets_all_hosts(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R1
        resp = self.get('/v1/hosts?region=1')
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_non_existing_region_raises404(self, fake_hosts):
        fake_hosts.side_effect = exceptions.NotFound()
        resp = self.get('/v1/hosts?region=5')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_name_filters(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get('/v1/hosts?region=1&name=www.example.net')
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), len(host_resp))
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_with_valid_data(self, mock_host):
        mock_host.return_value = None
        data = {'name': 'www.host1.com', 'region_id': '1', 'project_id': '1',
                'ip_address': '10.0.0.1', 'device_type': 'server'}
        resp = self.post('/v1/hosts', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_returns_host_obj(self, mock_host):
        return_value = {'name': 'www.host1.com', 'region_id': '1',
                        'project_id': '1', 'ip_address': '10.0.0.1', 'id': 1,
                        'device_type': 'server'}
        mock_host.return_value = return_value
        data = {'name': 'www.host1.com', 'region_id': '1', 'project_id': '1',
                'ip_address': '10.0.0.1', 'device_type': 'server'}
        resp = self.post('v1/hosts', data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(return_value, resp.json)
