import mock
import uuid

from oslo_serialization import jsonutils

from craton import api
from craton import exceptions
from craton.api import middleware
from craton.db.sqlalchemy import api as dbapi
from craton.tests import TestCase
from craton.tests.unit import fake_resources

project_id1 = uuid.uuid4().hex


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

    def put(self, path, data, **kw):
        content = jsonutils.dumps(data)
        content_type = 'application/json'
        resp = self.client.put(path=path, content_type=content_type,
                               data=content)
        resp.json = jsonutils.loads(resp.data.decode('utf-8'))
        return resp

    def delete(self, path, data=None):
        if data:
            content = jsonutils.dumps(data)
        else:
            content = None
        resp = self.client.delete(path=path, data=content)
        return resp


class APIV1WithContextTest(TestCase):
    def setUp(self):
        super(APIV1WithContextTest, self).setUp()
        self.app = api.setup_app()
        self.app.wsgi_app = middleware.LocalAuthContextMiddleware(
            self.app.wsgi_app)
        self.client = self.app.test_client()

    def get(self, path, **kw):
        resp = self.client.get(path=path, **kw)
        resp.json = jsonutils.loads(resp.data.decode('utf-8'))
        return resp


class APIV1MiddlewareTest(APIV1WithContextTest):
    def test_no_auth_token_returns_401(self):
        resp = self.get('v1/cells/1')
        self.assertEqual(401, resp.status_code)

    def test_ensure_non_uuid_token_returns_401(self):
        headers = {"X-Auth-Project": "abcd", "X-Auth-Token": "abcd123"}
        resp = self.get('v1/cells/1', headers=headers)
        self.assertEqual(401, resp.status_code)

    @mock.patch.object(dbapi, 'cells_get_by_id')
    @mock.patch.object(dbapi, 'get_user_info')
    def test_ensure_valid_uuid_is_processed(self, mock_user, mock_cell):
        mock_user.return_value = fake_resources.USER1
        mock_cell.return_value = fake_resources.CELL1
        headers = {"X-Auth-Project": "2757a1b4-cd90-4891-886c-a246fd4e7064",
                   "X-Auth-Token": "xx-yy-zz"}
        resp = self.get('v1/cells/1', headers=headers)
        self.assertEqual(200, resp.status_code)


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
        self.assertEqual(204, resp.status_code)


class APIV1CellsTest(APIV1Test):
    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL_LIST
        resp = self.get('v1/cells')
        self.assertEqual(len(resp.json), len(fake_resources.CELL_LIST))

    @mock.patch.object(dbapi, 'cells_get_by_name')
    def test_get_cells_with_name_filters(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL1
        resp = self.get('v1/cells?region_id=1&name=cell1')
        self.assertEqual(len(resp.json), 1)
        # Ensure we got the right cell
        self.assertEqual(resp.json[0]["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_by_id')
    def test_get_cells_with_id_filters(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL1
        resp = self.get('v1/cells?region_id=1&id=1')
        self.assertEqual(len(resp.json), 1)
        # Ensure we got the right cell
        self.assertEqual(resp.json[0]["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells_with_vars_filters(self, mock_cells):
        mock_cells.return_value = [fake_resources.CELL1]
        resp = self.get('v1/cells?region_id=1&vars=somekey:somevalue')
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_by_name')
    def test_get_cell_no_exist_by_name_fails(self, mock_cell):
        err = exceptions.NotFound()
        mock_cell.side_effect = err
        resp = self.get('v1/cells?region_id=1&name=dontexist')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_with_valid_data(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        data = {'name': 'cell1', 'region_id': 1}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_returns_cell_obj(self, mock_cell):
        return_value = {'name': 'cell1', 'region_id': 1, 'id': 1,
                        'variables': {}}
        mock_cell.return_value = return_value
        data = {'name': 'cell1', 'region_id': 1}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(return_value, resp.json)

    @mock.patch.object(dbapi, 'cells_update')
    def test_update_cell(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        payload = {'name': 'cell1-New', 'region_id': 1, 'project_id': 1}
        resp = self.put('v1/cells/1', data=payload)
        self.assertEqual(resp.json['region_id'], payload['region_id'])
        self.assertEqual(resp.json['project_id'], payload['project_id'])
        self.assertTrue(resp.json['name'], payload['name'])
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_fails_with_invalid_data(self, mock_cell):
        mock_cell.return_value = None
        # data is missing required cell name
        data = {'region_id': 1}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(422, resp.status_code)


class APIV1CellsVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'cells_get_by_id')
    def test_cells_get_variables(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        resp = self.get('v1/cells/1/variables')
        expected = {"variables": {"key1": "value1", "key2": "value2"}}
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'cells_variables_update')
    def test_cells_put_variables(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        payload = {"a": "b"}
        resp = self.put('v1/cells/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'cells_variables_delete')
    def test_cells_delete_variables(self, mock_cell):
        payload = {"key1": "value1"}
        resp = self.delete('v1/cells/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)


class APIV1RegionsIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'regions_get_by_id')
    def test_regions_get_by_id(self, mock_regions):
        mock_regions.return_value = fake_resources.REGION1
        resp = self.get('v1/regions/1')
        self.assertEqual(resp.json['name'], fake_resources.REGION1.name)

    @mock.patch.object(dbapi, 'regions_get_by_id')
    def test_regions_get_by_bad_id_is_404(self, mock_regions):
        mock_regions.side_effect = exceptions.NotFound()
        resp = self.get('v1/regions/1')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'regions_delete')
    def test_delete_region(self, mock_region):
        resp = self.delete('v1/regions/1')
        self.assertEqual(204, resp.status_code)


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

    @mock.patch.object(dbapi, 'regions_get_all')
    def test_regions_get_by_vars_filters(self, mock_regions):
        mock_regions.return_value = [fake_resources.REGION1]
        resp = self.get('v1/regions?vars=somekey:somevalue')
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], fake_resources.REGION1.name)

    @mock.patch.object(dbapi, 'regions_get_by_name')
    def test_get_region_no_exist_by_name_fails(self, mock_regions):
        mock_regions.side_effect = exceptions.NotFound()
        resp = self.get('v1/regions?name=bla')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'regions_create')
    def test_post_region_with_valid_data(self, mock_region):
        mock_region.return_value = fake_resources.REGION1
        data = {'name': 'region1'}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'regions_create')
    def test_create_region_returns_region_obj(self, mock_region):
        return_value = {'name': 'region1',
                        'variables': {"key1": "value1", "key2": "value2"}}
        fake_region = fake_resources.REGION1
        fake_region.variables = {"key1": "value1", "key2": "value2"}
        mock_region.return_value = fake_region
        data = {'name': 'region1',
                'variables': {"key1": "value1", "key2": "value2"}}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(return_value, resp.json)

    @mock.patch.object(dbapi, 'regions_update')
    def test_update_region(self, mock_region):
        mock_region.return_value = fake_resources.REGION1
        payload = {"name": "region_New1"}
        resp = self.put('v1/regions/1', data=payload)
        self.assertTrue(resp.json['name'], payload['name'])
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'regions_create')
    def test_post_region_with_invalid_data_fails(self, mock_region):
        mock_region.return_value = None
        data = {}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(422, resp.status_code)


class APIV1RegionsVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'regions_get_by_id')
    def test_region_get_variables(self, mock_region):
        mock_region.return_value = fake_resources.REGION1
        resp = self.get('v1/regions/1/variables')
        expected = {"variables": {"key1": "value1", "key2": "value2"}}
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'regions_variables_update')
    def test_regions_put_variables(self, mock_region):
        mock_region.return_value = fake_resources.REGION1
        payload = {"a": "b"}
        resp = self.put('v1/regions/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'regions_variables_delete')
    def test_regions_delete_variables(self, mock_region):
        payload = {"key1": "value1"}
        resp = self.delete('v1/regions/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)


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

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_resolved_vars(self, mock_host):
        region_vars = {"r_var": "one"}
        host = fake_resources.HOST1
        host.resolved.update(region_vars)
        expected = {"r_var": "one", "key1": "value1", "key2": "value2"}
        mock_host.return_value = host
        resp = self.get('v1/hosts/1')
        self.assertEqual(resp.json["variables"], expected)

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_no_resolved_vars(self, mock_host):
        region_vars = {"r_var": "one"}
        host = fake_resources.HOST1
        host.resolved.update(region_vars)
        expected = {"key1": "value1", "key2": "value2"}
        mock_host.return_value = host
        resp = self.get('v1/hosts/1?resolved-values=false')
        self.assertEqual(resp.json["variables"], expected)

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_labels(self, mock_host):
        mock_host.return_value = fake_resources.HOST4
        resp = self.get('v1/hosts/1/labels')
        self.assertEqual(resp.json["labels"], ["a", "b"])

    @mock.patch.object(dbapi, 'hosts_labels_update')
    def test_put_hosts_labels(self, mock_host):
        payload = {"labels": ["a", "b"]}
        mock_host.return_value = fake_resources.HOST4
        resp = self.put('v1/hosts/1/labels', data=payload)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json, payload)


class APIV1HostsTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_hosts_by_region_gets_all_hosts(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R1
        resp = self.get('/v1/hosts?region_id=1')
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_non_existing_region_raises404(self, fake_hosts):
        fake_hosts.side_effect = exceptions.NotFound()
        resp = self.get('/v1/hosts?region_id=5')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_name_filters(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get('/v1/hosts?region_id=1&name=www.example.net')
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), len(host_resp))
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_ip_address_filter(self, fake_hosts):
        region_id = 1
        ip_address = '10.10.0.1'
        filters = {
            'region_id': region_id, 'ip_address': ip_address, 'limit': 1000
        }
        path_query = '/v1/hosts?region_id={}&ip_address={}'.format(
            region_id, ip_address
        )
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get(path_query)
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

        fake_hosts.assert_called_once_with(mock.ANY, region_id, filters)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_vars_filters(self, fake_hosts):
        fake_hosts.return_value = [fake_resources.HOST1]
        resp = self.get('/v1/hosts?region_id=1&vars=somekey:somevalue')
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], fake_resources.HOST1.name)

    @mock.patch.object(dbapi, 'hosts_get_by_region')
    def test_get_host_by_label_filters(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get('/v1/hosts?region_id=1&label=somelabel')
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), len(host_resp))
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_with_valid_data(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        data = {'name': 'www.host1.com', 'region_id': 1,
                'ip_address': '10.0.0.1', 'device_type': 'server',
                'active': True}
        resp = self.post('/v1/hosts', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_update')
    def test_update_host(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        payload = {'name': 'Host_New', 'project_id': 1, 'region_id': 1,
                   'ip_address': "192.168.1.1", 'device_type': "server"}
        resp = self.put('/v1/hosts/1', data=payload)
        self.assertEqual(resp.json['project_id'], payload['project_id'])
        self.assertEqual(resp.json['region_id'], payload['region_id'])
        self.assertTrue(resp.json['name'], payload['name'])
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_returns_host_obj(self, mock_host):
        return_value = {'name': 'www.host1.com', 'region_id': 1,
                        'ip_address': '10.0.0.1', 'id': 1, 'variables': {},
                        'device_type': 'server', 'active': True}
        mock_host.return_value = return_value
        data = {'name': 'www.host1.com', 'region_id': 1,
                'ip_address': '10.0.0.1', 'device_type': 'server'}
        resp = self.post('v1/hosts', data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(return_value, resp.json)


class APIV1HostsVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_host_get_variables(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        resp = self.get('v1/hosts/1/variables?resolved-values=false')
        expected = {"variables": {"key1": "value1", "key2": "value2"}}
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_host_get_resolved_variables(self, mock_host):
        region_vars = {"r_var": "somevar"}
        host = fake_resources.HOST1
        host.resolved.update(region_vars)
        expected = {"r_var": "somevar", "key1": "value1", "key2": "value2"}
        mock_host.return_value = host
        resp = self.get('v1/hosts/1/variables')
        self.assertEqual(resp.json["variables"], expected)

    @mock.patch.object(dbapi, 'hosts_variables_update')
    def test_hosts_put_data(self, mock_host):
        mock_host.return_value = fake_resources.REGION1
        payload = {"a": "b"}
        resp = self.put('v1/hosts/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'hosts_variables_delete')
    def test_regions_delete_data(self, mock_host):
        payload = {"key1": "value1"}
        resp = self.delete('v1/hosts/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)


class APIV1ProjectsTest(APIV1Test):
    @mock.patch.object(dbapi, 'projects_create')
    def test_create_project(self, mock_project):
        return_value = {'name': 'project1', 'id': 1}
        mock_project.return_value = return_value
        data = {'name': 'project1'}
        resp = self.post('v1/projects', data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['id'], 1)

    @mock.patch.object(dbapi, 'projects_get_all')
    def test_project_get_all(self, mock_projects):
        proj1 = fake_resources.PROJECT1
        proj2 = fake_resources.PROJECT2
        return_value = [proj1, proj2]
        mock_projects.return_value = return_value

        resp = self.get('v1/projects')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'projects_get_all')
    def test_projects_get_no_admin_fails(self, mock_project):
        mock_project.side_effect = exceptions.AdminRequired()
        resp = self.get('v1/projects')
        self.assertEqual(resp.status_code, 401)


class APIV1UsersTest(APIV1Test):
    @mock.patch.object(dbapi, 'users_create')
    @mock.patch.object(dbapi, 'projects_get_by_id')
    def test_create_users(self, mock_project, mock_user):
        mock_project.return_value = {'id': project_id1, 'name': 'project1'}
        return_value = {'name': 'user1', 'is_admin': False, 'id': 1,
                        'api_key': 'xxxx'}
        mock_user.return_value = return_value
        data = {'name': 'user1', 'is_admin': False}
        resp = self.post('v1/users', data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['id'], 1)

    @mock.patch.object(dbapi, 'users_get_all')
    def test_users_get_all(self, mock_user):
        return_values = [fake_resources.USER1, fake_resources.USER2]
        mock_user.return_value = return_values
        resp = self.get('v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'users_get_all')
    def test_users_get_no_admin_fails(self, mock_user):
        mock_user.side_effect = exceptions.AdminRequired()
        resp = self.get('v1/users')
        self.assertEqual(resp.status_code, 401)


class APIV1NetworksTest(APIV1Test):
    @mock.patch.object(dbapi, 'networks_get_by_region')
    def test_networks_by_region_gets_all_networks(self, fake_network):
        fake_network.return_value = fake_resources.NETWORKS_LIST
        resp = self.get('/v1/networks?region_id=1')
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'networks_get_by_id')
    def test_networks_get_by_id(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        resp = self.get('v1/networks/1')
        self.assertEqual(resp.json["name"], fake_resources.NETWORK1.name)

    @mock.patch.object(dbapi, 'networks_get_by_id')
    def test_networks_get_by_bad_id_is_404(self, mock_network):
        mock_network.side_effect = exceptions.NotFound()
        resp = self.get('v1/networks/9')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'networks_get_by_region')
    def test_get_networks_by_non_existing_region_raises404(self, fake_network):
        fake_network.side_effect = exceptions.NotFound()
        resp = self.get('/v1/networks?region_id=5')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'networks_get_by_region')
    def test_get_networks_by_filters(self, fake_networks):
        fake_networks.return_value = [fake_resources.NETWORK1]
        resp = self.get('/v1/networks?region_id=1&name=PrivateNetwork')
        net_resp = fake_resources.NETWORK1
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], net_resp.name)

    @mock.patch.object(dbapi, 'networks_create')
    def test_create_networks_with_valid_data(self, mock_network):
        mock_network.return_value = None
        data = {'name': 'some network', 'region_id': 1,
                'cidr': '10.10.1.0/24', 'gateway': '192.168.1.1',
                'netmask': '255.255.255.0'}
        resp = self.post('/v1/networks', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'networks_create')
    def test_create_networks_with_invalid_data(self, mock_network):
        mock_network.return_value = None
        # data is missing entries
        data = {'region_id': 1}
        resp = self.post('v1/networks', data=data)
        self.assertEqual(422, resp.status_code)

    @mock.patch.object(dbapi, 'networks_update')
    def test_update_network(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        payload = {"name": "Network_New1"}
        resp = self.put('v1/networks/1', data=payload)
        self.assertTrue(resp.json['name'], payload['name'])
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'networks_delete')
    def test_delete_network(self, mock_network):
        resp = self.delete('v1/networks/1')
        self.assertEqual(204, resp.status_code)

    @mock.patch.object(dbapi, 'networks_variables_update')
    def test_networks_put_variables(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        payload = {"a": "b"}
        resp = self.put('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'networks_variables_update')
    def test_network_put_variable(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        payload = {"a": "b"}
        resp = self.put('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'networks_get_by_id')
    def test_network_get_variables(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK2
        resp = self.get('v1/networks/2/variables')
        expected = {"variables": {"pkey1": "pvalue1"}}
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'networks_variables_delete')
    def test_network_variables_delete(self, mock_network):
        payload = {"key1": "value1"}
        resp = self.delete('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)


class APIV1NetworkDevicesTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_devices_get_by_region')
    def test_get_network_devices_by_ip_address_filter(self, fake_devices):
        region_id = '1'
        ip_address = '10.10.0.1'
        filters = {'region_id': region_id, 'ip_address': ip_address}
        path_query = (
            '/v1/network_devices?region_id={}&ip_address={}'.format(
                region_id, ip_address
            )
        )
        fake_devices.return_value = fake_resources.NETWORK_DEVICE_LIST1
        resp = self.get(path_query)
        device_resp = fake_resources.NETWORK_DEVICE_LIST1
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["ip_address"],
                         device_resp[0].ip_address)
        fake_devices.assert_called_once_with(mock.ANY, region_id, filters)

    @mock.patch.object(dbapi, 'network_devices_get_by_region')
    def test_network_devices_get_by_region(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE_LIST1
        resp = self.get('/v1/network_devices/1')
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'network_devices_get_by_id')
    def test_get_network_devices_get_by_id(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.get('/v1/network_devices/1')
        self.assertEqual(resp.json["hostname"],
                         fake_resources.NETWORK_DEVICE1.hostname)

    @mock.patch.object(dbapi, 'network_devices_create')
    def test_create_network_devices_with_valid_data(self, mock_devices):
        mock_devices.return_value = None
        data = {'hostname': 'NewNetDevice1', 'region_id': 1,
                'device_type': 'Sample', 'ip_address': '0.0.0.0'}
        resp = self.post('/v1/network_devices', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'network_devices_create')
    def test_create_netdevices_with_invalid_data(self, mock_devices):
        mock_devices.return_value = None
        # data is missing entry
        data = {'hostname': 'Sample'}
        resp = self.post('/v1/network_devices', data=data)
        self.assertEqual(422, resp.status_code)

    @mock.patch.object(dbapi, 'network_devices_delete')
    def test_delete_network_devices(self, mock_devices):
        resp = self.delete('v1/network_devices/1')
        self.assertEqual(204, resp.status_code)

    @mock.patch.object(dbapi, 'network_devices_variables_delete')
    def test_network_devices_variables_delete(self, mock_devices):
        payload = {"key1": "value1"}
        resp = self.delete('v1/network_devices/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)

    @mock.patch.object(dbapi, 'network_devices_variables_update')
    def test_network_devices_variables_update(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        payload = {"a": "b"}
        resp = self.put('v1/network_devices/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)

    @mock.patch.object(dbapi, 'network_devices_labels_update')
    def test_network_devices_labels_update(self, mock_devices):
        payload = {"labels": ["a", "b"]}
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.put('v1/network_devices/1/labels', data=payload)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json, payload)


class APIV1NetworkInterfacesTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_interfaces_get_by_device')
    def test_get_netinterfaces_by_ip_address_filter(self, fake_interfaces):
        device_id = 1
        ip_address = '10.10.0.1'
        filters = {'device_id': device_id, 'ip_address': ip_address}
        path_query = (
            '/v1/network_interfaces?device_id={}&ip_address={}'.format(
                device_id, ip_address
            )
        )
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE_LIST1
        resp = self.get(path_query)
        interface_resp = fake_resources.NETWORK_INTERFACE_LIST1
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], interface_resp[0].name)

        fake_interfaces.assert_called_once_with(mock.ANY, device_id, filters)

    @mock.patch.object(dbapi, 'network_interfaces_get_by_device')
    def test_get_network_interfaces_by_device_id(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE_LIST1
        resp = self.get('/v1/network_interfaces?name=NetInterface&device_id=1')
        network_interface_resp = fake_resources.NETWORK_INTERFACE1
        self.assertEqual(resp.json[0]["name"], network_interface_resp.name)

    @mock.patch.object(dbapi, 'network_interfaces_get_by_id')
    def test_get_network_interfaces_by_id(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE1
        resp = self.get('/v1/network_interfaces/1')
        self.assertEqual(resp.json["name"],
                         fake_resources.NETWORK_INTERFACE1.name)

    @mock.patch.object(dbapi, 'network_interfaces_create')
    def test_network_interfaces_create_with_valid_data(self, fake_interfaces):
        fake_interfaces.return_value = None
        data = {'name': 'NewNetInterface', 'device_id': 1,
                'ip_address': '0.0.0.0', 'interface_type': 'Sample'}
        resp = self.post('/v1/network_interfaces', data=data)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'network_interfaces_create')
    def test_network_interfaces_create_invalid_data(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE1
        # data is missing entry
        data = {'name': 'sample'}
        resp = self.post('/v1/network_interfaces', data=data)
        self.assertEqual(422, resp.status_code)

    @mock.patch.object(dbapi, 'network_interfaces_update')
    def test_network_interfaces_update(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE1
        payload = {'name': 'New', 'device_id': 1, 'project_id': 1,
                   'interface_type': 'interface_type1',
                   'ip_address': '10.0.0.1'}
        resp = self.put('/v1/network_interfaces/1', data=payload)
        self.assertEqual(resp.json['project_id'], payload['project_id'])
        self.assertEqual(resp.json['device_id'], payload['device_id'])
        self.assertTrue(resp.json['name'], payload['name'])
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(dbapi, 'network_interfaces_delete')
    def test_network_interfaces_delete(self, fake_interfaces):
        resp = self.delete('/v1/network_interfaces/1')
        self.assertEqual(204, resp.status_code)
