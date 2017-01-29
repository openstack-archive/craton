import copy
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
            content_type = 'application/json'
        else:
            content = None
            content_type = None
        resp = self.client.delete(
            path=path, content_type=content_type, data=content
        )
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

    @mock.patch.object(dbapi, 'cells_update')
    def test_put_cells_by_id(self, mock_cell):
        data = {'note': 'new note', 'name': 'new name'}
        resp = self.put('v1/cells/1', data=data)
        self.assertEqual(200, resp.status_code)
        mock_cell.assert_called_once_with(mock.ANY, '1', data)

    @mock.patch.object(dbapi, 'cells_update')
    def test_put_cells_by_id_invalid_property(self, mock_cell):
        data = {'foo': 'isinvalid'}
        resp = self.put('v1/cells/1', data=data)
        self.assertEqual(200, resp.status_code)
        mock_cell.assert_called_once_with(mock.ANY, '1', {})

    @mock.patch.object(dbapi, 'cells_update')
    def test_update_cell(self, mock_cell):
        record = dict(fake_resources.CELL1.items())
        payload = {'name': 'cell1-New'}
        record.update(payload)
        db_data = payload.copy()
        mock_cell.return_value = record

        resp = self.put('v1/cells/1', data=payload)

        self.assertEqual(resp.json['name'], db_data['name'])
        self.assertEqual(200, resp.status_code)
        mock_cell.assert_called_once_with(mock.ANY, '1', db_data)


class APIV1CellsTest(APIV1Test):
    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL_LIST
        resp = self.get('v1/cells')
        self.assertEqual(len(resp.json), len(fake_resources.CELL_LIST))
        mock_cells.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells_invalid_property(self, mock_cells):
        mock_cells.return_value = fake_resources.CELL_LIST
        resp = self.get('v1/cells?foo=isaninvalidproperty')
        self.assertEqual(len(resp.json), len(fake_resources.CELL_LIST))
        mock_cells.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells_with_name_filters(self, mock_cells):
        cell_name = 'cell1'
        mock_cells.return_value = fake_resources.CELL_LIST2
        resp = self.get('v1/cells?name={}'.format(cell_name))
        self.assertEqual(len(resp.json), 2)
        # Ensure we got the right cell
        self.assertEqual(resp.json[0]["name"], cell_name)
        self.assertEqual(resp.json[1]["name"], cell_name)

    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells_with_name_and_region_filters(self, mock_cells):
        mock_cells.return_value = [fake_resources.CELL1]
        resp = self.get('v1/cells?region_id=1&name=cell1')
        self.assertEqual(len(resp.json), 1)
        # Ensure we got the right cell
        self.assertEqual(resp.json[0]["name"], fake_resources.CELL1.name)

    @mock.patch.object(dbapi, 'cells_get_all')
    def test_get_cells_with_id_filters(self, mock_cells):
        mock_cells.return_value = [fake_resources.CELL1]
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

    @mock.patch.object(dbapi, 'cells_get_all')
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
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_returns_cell_obj(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        data = {
            'name': "cell1",
            'region_id': 1,
            'variables': {'key1': 'value1', 'key2': 'value2'},
        }
        resp = self.post('v1/cells', data=data)

        expected_result = {
            'id': 1,
            'name': 'cell1',
            'region_id': 1,
            'project_id': 1,
            'variables': {'key1': 'value1', 'key2': 'value2'},
        }
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected_result, resp.json)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_fails_with_invalid_data(self, mock_cell):
        mock_cell.return_value = None
        # data is missing required cell name
        data = {'region_id': 1}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(422, resp.status_code)

    @mock.patch.object(dbapi, 'cells_create')
    def test_create_cell_with_invalid_property(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        data = {'name': 'cell1', 'region_id': 1, 'foo': 'invalidproperty'}
        resp = self.post('v1/cells', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)
        mock_cell.assert_called_once_with(
            mock.ANY, {'name': 'cell1', 'region_id': 1, 'project_id': None}
        )


class APIV1CellsVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'cells_get_by_id')
    def test_cells_get_variables(self, mock_cell):
        mock_cell.return_value = fake_resources.CELL1
        resp = self.get('v1/cells/1/variables')
        expected = {"variables": {"key1": "value1", "key2": "value2"}}
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'cells_variables_update')
    def test_cells_put_variables(self, mock_cell):
        db_return_value = copy.deepcopy(fake_resources.CELL1)
        db_return_value.variables["a"] = "b"
        mock_cell.return_value = db_return_value
        payload = {"a": "b"}
        db_data = payload.copy()
        resp = self.put('v1/cells/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)
        mock_cell.assert_called_once_with(mock.ANY, '1', db_data)
        expected = {
            "variables": {"key1": "value1", "key2": "value2", "a": "b"},
        }
        self.assertDictEqual(expected, resp.json)

    @mock.patch.object(dbapi, 'cells_variables_update')
    def test_cells_put_bad_data_type(self, mock_cell):
        payload = ["a", "b"]
        resp = self.put('v1/cells/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_cell.assert_not_called()

    @mock.patch.object(dbapi, 'cells_variables_delete')
    def test_cells_delete_variables(self, mock_cell):
        payload = {"key1": "value1"}
        db_data = payload.copy()
        resp = self.delete('v1/cells/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_cell.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'cells_variables_delete')
    def test_cells_delete_bad_data_type(self, mock_cell):
        payload = ["a", "b"]
        resp = self.delete('v1/cells/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_cell.assert_not_called()


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

    @mock.patch.object(dbapi, 'regions_update')
    def test_put_regions_by_id(self, mock_region):
        data = {'note': 'new note', 'name': 'new name'}
        resp = self.put('v1/regions/1', data=data)
        self.assertEqual(200, resp.status_code)
        mock_region.assert_called_once_with(mock.ANY, '1', data)

    @mock.patch.object(dbapi, 'regions_update')
    def test_put_regions_by_id_invalid_property(self, mock_region):
        data = {'foo': 'isinvalid'}
        resp = self.put('v1/regions/1', data=data)
        self.assertEqual(200, resp.status_code)
        mock_region.assert_called_once_with(mock.ANY, '1', {})

    @mock.patch.object(dbapi, 'regions_update')
    def test_update_region(self, mock_region):
        record = dict(fake_resources.REGION1.items())
        payload = {"name": "region_New1"}
        db_data = payload.copy()
        record.update(payload)
        mock_region.return_value = record

        resp = self.put('v1/regions/1', data=payload)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['name'], 'region_New1')
        mock_region.assert_called_once_with(mock.ANY, '1', db_data)


class APIV1RegionsTest(APIV1Test):
    @mock.patch.object(dbapi, 'regions_get_all')
    def test_regions_get_all(self, mock_regions):
        mock_regions.return_value = fake_resources.REGIONS_LIST
        resp = self.get('v1/regions')
        self.assertEqual(len(resp.json), len(fake_resources.REGIONS_LIST))

    @mock.patch.object(dbapi, 'regions_get_all')
    def test_regions_get_all_by_invalid_property_name(self, mock_regions):
        mock_regions.return_value = fake_resources.REGIONS_LIST
        resp = self.get('v1/regions?foo=invalidpropertyname')
        self.assertEqual(len(resp.json), len(fake_resources.REGIONS_LIST))
        mock_regions.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

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
        self.assertEqual(201, resp.status_code)

    @mock.patch.object(dbapi, 'regions_create')
    def test_post_region_with_invalid_property_name(self, mock_region):
        mock_region.return_value = fake_resources.REGION1
        data = {'name': 'region1', 'foo': 'invalidpropertyname'}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(201, resp.status_code)
        mock_region.assert_called_once_with(
            mock.ANY,
            {'project_id': None, 'name': 'region1'}
        )

    @mock.patch.object(dbapi, 'regions_create')
    def test_create_region_returns_region_obj(self, mock_region):
        return_value = {'name': 'region1',
                        'project_id': 'abcd',
                        'id': 1,
                        'variables': {"key1": "value1", "key2": "value2"}}
        fake_region = fake_resources.REGION1
        fake_region.variables = {"key1": "value1", "key2": "value2"}
        mock_region.return_value = fake_region
        data = {'name': 'region1',
                'variables': {"key1": "value1", "key2": "value2"}}
        resp = self.post('v1/regions', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertEqual(return_value, resp.json)

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
        db_return_value = copy.deepcopy(fake_resources.REGION1)
        db_return_value.variables["a"] = "b"
        mock_region.return_value = db_return_value
        payload = {"a": "b"}
        db_data = payload.copy()
        resp = self.put('v1/regions/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)
        mock_region.assert_called_once_with(mock.ANY, '1', db_data)
        expected = {
            "variables": {"key1": "value1", "key2": "value2", "a": "b"},
        }
        self.assertDictEqual(expected, resp.json)

    @mock.patch.object(dbapi, 'regions_variables_update')
    def test_regions_put_bad_data_type(self, mock_region):
        payload = ["a", "b"]
        resp = self.put('v1/regions/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_region.assert_not_called()

    @mock.patch.object(dbapi, 'regions_variables_delete')
    def test_regions_delete_variables(self, mock_region):
        payload = {"key1": "value1"}
        db_data = payload.copy()
        resp = self.delete('v1/regions/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_region.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'regions_variables_delete')
    def test_regions_delete_bad_data_type(self, mock_region):
        payload = ["a", "b"]
        resp = self.delete('v1/regions/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_region.assert_not_called()


class APIV1HostsIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_by_id(self, mock_hosts):
        mock_hosts.return_value = fake_resources.HOST1
        resp = self.get('v1/hosts/1')
        self.assertEqual(resp.json["name"], fake_resources.HOST1.name)

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_get_hosts_by_id_invalid_property_name(self, mock_hosts):
        mock_hosts.return_value = fake_resources.HOST1
        resp = self.get('/v1/hosts/1?foo=invalidproperty')
        self.assertEqual(resp.json["name"], fake_resources.HOST1.name)
        mock_hosts.assert_called_once_with(mock.ANY, "1")

    @mock.patch.object(dbapi, 'hosts_update')
    def test_put_hosts_by_id_invalid_property_name(self, mock_hosts):
        mock_hosts.return_value = fake_resources.HOST1
        resp = self.put('/v1/hosts/1', data={'foo': 'invalidproperty'})
        self.assertEqual(resp.json["name"], fake_resources.HOST1.name)
        mock_hosts.assert_called_once_with(
            mock.ANY, "1", {}
        )

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

    @mock.patch.object(dbapi, 'hosts_update')
    def test_update_host(self, mock_host):
        record = dict(fake_resources.HOST1.items())
        payload = {'name': 'Host_New'}
        db_data = payload.copy()
        record.update(payload)
        mock_host.return_value = record

        resp = self.put('/v1/hosts/1', data=payload)

        self.assertEqual(resp.json['name'], db_data['name'])
        self.assertEqual(200, resp.status_code)
        mock_host.assert_called_once_with(mock.ANY, '1', db_data)


class APIV1HostsLabelsTest(APIV1Test):
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

    @mock.patch.object(dbapi, 'hosts_labels_update')
    def test_put_hosts_labels_invalid_property_name(self, mock_host):
        req_data = {"labels": ["a", "b"], "foo": ["should", "be", "removed"]}
        resp_data = {"labels": ["a", "b"]}
        mock_host.return_value = fake_resources.HOST4
        resp = self.put('v1/hosts/1/labels', data=req_data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json, resp_data)
        mock_host.assert_called_once_with(mock.ANY, '1', resp_data)

    @mock.patch.object(dbapi, 'hosts_labels_update')
    def test_put_hosts_labels_validate_type(self, mock_host):
        payload = {"labels": {"a": "b"}}
        mock_host.return_value = fake_resources.HOST4
        resp = self.put('v1/hosts/1/labels', data=payload)
        self.assertEqual(422, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_labels_delete')
    def test_hosts_delete_labels(self, mock_host):
        payload = {"labels": ["label1", "label2"]}
        db_data = payload.copy()
        resp = self.delete('v1/hosts/1/labels', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_host.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'hosts_labels_delete')
    def test_hosts_delete_bad_data_type(self, mock_host):
        payload = ["label1", "label2"]
        resp = self.delete('v1/hosts/1/labels', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_host.assert_not_called()


class APIV1HostsTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_hosts_by_region_gets_all_hosts(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R1
        resp = self.get('/v1/hosts?region_id=1')
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_hosts_invalid_property_name(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R1
        resp = self.get('/v1/hosts?foo=invalidproperty')
        self.assertEqual(len(resp.json), 2)
        fake_hosts.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_host_by_non_existing_region_raises404(self, fake_hosts):
        fake_hosts.side_effect = exceptions.NotFound()
        resp = self.get('/v1/hosts?region_id=5')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_hosts(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R3
        resp = self.get('/v1/hosts')
        self.assertEqual(len(resp.json), 3)
        fake_hosts.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_host_by_name_filters(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get('/v1/hosts?region_id=1&name=www.example.net')
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), len(host_resp))
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_host_by_ip_address_filter(self, fake_hosts):
        region_id = 1
        ip_address = '10.10.0.1'
        filters = {
            'region_id': 1, 'ip_address': ip_address,
        }
        path_query = '/v1/hosts?region_id={}&ip_address={}'.format(
            region_id, ip_address
        )
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get(path_query)
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

        fake_hosts.assert_called_once_with(
            mock.ANY, filters, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_host_by_vars_filters(self, fake_hosts):
        fake_hosts.return_value = [fake_resources.HOST1]
        resp = self.get('/v1/hosts?region_id=1&vars=somekey:somevalue')
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], fake_resources.HOST1.name)

    @mock.patch.object(dbapi, 'hosts_get_all')
    def test_get_host_by_label_filters(self, fake_hosts):
        fake_hosts.return_value = fake_resources.HOSTS_LIST_R2
        resp = self.get('/v1/hosts?region_id=1&label=somelabel')
        host_resp = fake_resources.HOSTS_LIST_R2
        self.assertEqual(len(resp.json), len(host_resp))
        self.assertEqual(resp.json[0]["name"], host_resp[0].name)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_with_valid_data(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        data = {'name': 'www.craton.com', 'region_id': 1,
                'ip_address': '192.168.1.1', 'device_type': 'server',
                'active': True}
        resp = self.post('/v1/hosts', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_returns_host_obj(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        data = {
            'name': 'www.craton.com',
            'region_id': 1,
            'ip_address': '192.168.1.1',
            'device_type': 'server',
            'labels': [],
            'variables': {"key1": "value1", "key2": "value2"},
        }
        resp = self.post('v1/hosts', data=data)
        self.assertEqual(201, resp.status_code)
        expected_response = {
            'id': 1,
            'name': 'www.craton.com',
            'region_id': 1,
            'project_id': 1,
            'ip_address': '192.168.1.1',
            'device_type': 'server',
            'labels': [],
            'variables': {"key1": "value1", "key2": "value2"},
        }
        self.assertEqual(expected_response, resp.json)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'hosts_create')
    def test_create_host_invalid_property_name(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        data = {'name': 'www.craton.com', 'region_id': 1, 'foo': 'invalidprop',
                'ip_address': '192.168.1.1', 'device_type': 'server'}
        db_json = data.copy()
        db_json['project_id'] = None
        del db_json['foo']

        resp = self.post('v1/hosts', data=data)

        expected_result = {
            'device_type': 'server',
            'id': 1,
            'ip_address': '192.168.1.1',
            'labels': [],
            'name': 'www.craton.com',
            'region_id': 1,
            'project_id': 1,
            'variables': {},
        }

        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected_result, resp.json)
        self.assertIn('Location', resp.headers)
        mock_host.assert_called_once_with(mock.ANY, db_json)


class APIV1HostsVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_host_get_variables(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        resp = self.get('v1/hosts/1/variables?resolved-values=false')
        expected = {"variables": {"key1": "value1", "key2": "value2"}}
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'hosts_get_by_id')
    def test_host_get_variables_invalid_property_name(self, mock_host):
        mock_host.return_value = fake_resources.HOST1
        resp = self.get('v1/hosts/1/variables?foo=isnotreal')
        expected = {
            "variables": {
                "r_var": "somevar",
                "key1": "value1",
                "key2": "value2",
            }
        }
        self.assertEqual(expected, resp.json)
        self.assertEqual(resp.status_code, 200)
        mock_host.assert_called_once_with(mock.ANY, "1")

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
        db_return_value = copy.deepcopy(fake_resources.HOST1)
        db_return_value.variables["a"] = "b"
        mock_host.return_value = db_return_value
        payload = {"a": "b"}
        db_data = payload.copy()
        resp = self.put('v1/hosts/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)
        mock_host.assert_called_once_with(mock.ANY, '1', db_data)
        expected = {
            "variables": {"key1": "value1", "key2": "value2", "a": "b"},
        }
        self.assertDictEqual(expected, resp.json)

    @mock.patch.object(dbapi, 'hosts_variables_update')
    def test_hosts_put_bad_data_type(self, mock_host):
        payload = ["a", "b"]
        resp = self.put('v1/hosts/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_host.assert_not_called()

    @mock.patch.object(dbapi, 'hosts_variables_delete')
    def test_hosts_delete_data(self, mock_host):
        payload = {"key1": "value1"}
        db_data = payload.copy()
        resp = self.delete('v1/hosts/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_host.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'hosts_variables_delete')
    def test_hosts_delete_bad_data_type(self, mock_host):
        payload = ["a", "b"]
        resp = self.delete('v1/hosts/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_host.assert_not_called()


class APIV1ProjectsTest(APIV1Test):
    @mock.patch.object(dbapi, 'projects_create')
    def test_create_project(self, mock_project):
        mock_project.return_value = fake_resources.PROJECT1
        data = {'name': 'project1'}
        resp = self.post('v1/projects', data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['id'], 1)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'projects_get_all')
    def test_project_get_all(self, mock_projects):
        proj1 = fake_resources.PROJECT1
        proj2 = fake_resources.PROJECT2
        return_value = [proj1, proj2]
        mock_projects.return_value = return_value

        resp = self.get('v1/projects')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'projects_create')
    def test_project_post_invalid_property(self, mock_projects):
        data = {'foo': 'isinvalidproperty'}
        resp = self.post('v1/projects', data=data)
        self.assertEqual(resp.status_code, 201)
        mock_projects.assert_called_once_with(mock.ANY, {})

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
        mock_user.return_value = fake_resources.USER1
        data = {'username': 'user1', 'is_admin': False}
        resp = self.post('v1/users', data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['id'], 1)
        self.assertIn("Location", resp.headers)

    @mock.patch.object(dbapi, 'users_create')
    @mock.patch.object(dbapi, 'projects_get_by_id')
    def test_create_users_invalid_property(self, mock_project, mock_user):
        mock_project.return_value = {'id': project_id1, 'name': 'project1'}
        mock_user.return_value = fake_resources.USER1
        data = {
            'username': 'user1',
            'is_admin': False,
            'foo': 'isinvalidproperty',
        }
        resp = self.post('v1/users', data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['id'], 1)
        self.assertIn("Location", resp.headers)
        db_json = {'username': 'user1', 'is_admin': False, 'api_key': mock.ANY,
                   'project_id': None}
        mock_user.assert_called_once_with(mock.ANY, db_json)

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
    @mock.patch.object(dbapi, 'networks_get_all')
    def test_networks_by_region_gets_all_networks(self, fake_network):
        fake_network.return_value = fake_resources.NETWORKS_LIST
        resp = self.get('/v1/networks?region_id=1')
        self.assertEqual(len(resp.json), 2)

    @mock.patch.object(dbapi, 'networks_get_all')
    def test_get_networks_by_non_existing_region_raises404(self, fake_network):
        fake_network.side_effect = exceptions.NotFound()
        resp = self.get('/v1/networks?region_id=5')
        self.assertEqual(404, resp.status_code)

    @mock.patch.object(dbapi, 'networks_get_all')
    def test_get_networks_by_filters(self, fake_networks):
        fake_networks.return_value = [fake_resources.NETWORK1]
        resp = self.get('/v1/networks?region_id=1&name=PrivateNetwork')
        net_resp = fake_resources.NETWORK1
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], net_resp.name)

    @mock.patch.object(dbapi, 'networks_get_all')
    def test_get_networks(self, fake_networks):
        fake_networks.return_value = fake_resources.NETWORKS_LIST2
        resp = self.get('/v1/networks')
        self.assertEqual(len(resp.json), 3)
        fake_networks.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'networks_get_all')
    def test_get_networks_invalid_property(self, fake_networks):
        fake_networks.return_value = fake_resources.NETWORKS_LIST2
        resp = self.get('/v1/networks?foo=invalid')
        self.assertEqual(len(resp.json), 3)
        fake_networks.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'networks_create')
    def test_create_networks_with_valid_data(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        data = {
            'name': 'PrivateNetwork',
            'cidr': '192.168.1.0/24',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'variables': {'key1': 'value1'},
            'region_id': 1,
        }
        resp = self.post('/v1/networks', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'networks_create')
    def test_create_networks_with_invalid_data(self, mock_network):
        mock_network.return_value = None
        # data is missing entries
        data = {'region_id': 1}
        resp = self.post('v1/networks', data=data)
        self.assertEqual(422, resp.status_code)

    @mock.patch.object(dbapi, 'networks_create')
    def test_create_networks_with_invalid_property(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        data = {
            'cidr': '192.168.1.0/24',
            'gateway': '192.168.1.1',
            'name': 'PrivateNetwork',
            'netmask': '255.255.255.0',
            'region_id': 1,
            'variables': {'key1': 'value1'},
            'foo': 'isinvalid',
        }
        resp = self.post('/v1/networks', data=data)
        expected_response = {
            'cidr': '192.168.1.0/24',
            'gateway': '192.168.1.1',
            'id': 1,
            'name': 'PrivateNetwork',
            'netmask': '255.255.255.0',
            'region_id': 1,
            'project_id': 1,
            'variables': {'key1': 'value1'},
        }
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected_response, resp.json)
        mock_network.assert_called_once()
        self.assertIn('Location', resp.headers)


class APIV1NetworksIDTest(APIV1Test):
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

    @mock.patch.object(dbapi, 'networks_update')
    def test_update_network(self, mock_network):
        record = dict(fake_resources.NETWORK1.items())
        payload = {"name": "Network_New1"}
        db_data = payload.copy()
        record.update(payload)
        mock_network.return_value = record

        resp = self.put('v1/networks/1', data=payload)

        self.assertEqual(resp.json['name'], payload['name'])
        self.assertEqual(resp.status_code, 200)
        mock_network.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'networks_update')
    def test_update_network_invalid_property(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        payload = {"foo": "isinvalid"}
        resp = self.put('v1/networks/1', data=payload)
        self.assertEqual(resp.status_code, 200)
        mock_network.assert_called_once_with(mock.ANY, '1', {})

    @mock.patch.object(dbapi, 'networks_delete')
    def test_delete_network(self, mock_network):
        resp = self.delete('v1/networks/1')
        self.assertEqual(204, resp.status_code)


class APIV1NetworksVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'networks_get_by_id')
    def test_networks_get_variables(self, mock_network):
        mock_network.return_value = fake_resources.NETWORK1
        resp = self.get('v1/networks/1/variables')
        expected = {"variables": {"key1": "value1"}}
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'networks_variables_update')
    def test_networks_put_variables(self, mock_network):
        db_return_value = copy.deepcopy(fake_resources.NETWORK1)
        db_return_value.variables["a"] = "b"
        mock_network.return_value = db_return_value
        payload = {"a": "b"}
        db_data = payload.copy()
        resp = self.put('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)
        mock_network.assert_called_once_with(mock.ANY, '1', db_data)
        expected = {
            "variables": {"key1": "value1", "a": "b"},
        }
        self.assertDictEqual(expected, resp.json)

    @mock.patch.object(dbapi, 'networks_variables_update')
    def test_networks_put_bad_data_type(self, mock_network):
        payload = ["a", "b"]
        resp = self.put('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_network.assert_not_called()

    @mock.patch.object(dbapi, 'networks_variables_delete')
    def test_networks_delete_variables(self, mock_network):
        payload = {"key1": "value1"}
        db_data = payload.copy()
        resp = self.delete('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_network.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'networks_variables_delete')
    def test_networks_delete_bad_data_type(self, mock_network):
        payload = ["a", "b"]
        resp = self.delete('v1/networks/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_network.assert_not_called()


class APIV1NetworkDevicesIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_devices_get_by_id')
    def test_get_network_devices_by_id_invalid_property(self, fake_device):
        fake_device.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.get('/v1/network-devices/1?foo=isaninvalidproperty')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['hostname'], 'NetDevices1')
        fake_device.assert_called_once_with(mock.ANY, '1')

    @mock.patch.object(dbapi, 'network_devices_get_by_id')
    def test_get_network_devices_by_id(self, fake_device):
        fake_device.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.get('/v1/network-devices/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['hostname'], 'NetDevices1')
        fake_device.assert_called_once_with(mock.ANY, '1')

    @mock.patch.object(dbapi, 'network_devices_update')
    def test_put_network_device(self, fake_device):
        payload = {"hostname": "NetDev_New1"}
        fake_device.return_value = dict(fake_resources.NETWORK_DEVICE1.items(),
                                        **payload)
        resp = self.put('v1/network-devices/1', data=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['hostname'], "NetDev_New1")
        fake_device.assert_called_once_with(
            mock.ANY, '1', {"hostname": "NetDev_New1"}
        )

    @mock.patch.object(dbapi, 'network_devices_update')
    def test_put_network_device_invalid_property(self, fake_device):
        fake_device.return_value = fake_resources.NETWORK_DEVICE1
        payload = {"foo": "isinvalid"}
        resp = self.put('v1/network-devices/1', data=payload)
        self.assertEqual(resp.status_code, 200)
        fake_device.assert_called_once_with(mock.ANY, '1', {})

    @mock.patch.object(dbapi, 'network_devices_get_by_id')
    def test_get_network_devices_get_by_id(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.get('/v1/network-devices/1')
        self.assertEqual(resp.json["hostname"],
                         fake_resources.NETWORK_DEVICE1.hostname)

    @mock.patch.object(dbapi, 'network_devices_delete')
    def test_delete_network_devices(self, mock_devices):
        resp = self.delete('v1/network-devices/1')
        self.assertEqual(204, resp.status_code)


class APIV1NetworkDevicesTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_devices_get_all')
    def test_get_network_devices_by_ip_address_filter(self, fake_devices):
        region_id = '1'
        ip_address = '10.10.0.1'
        filters = {'region_id': region_id, 'ip_address': ip_address}
        path_query = '/v1/network-devices?region_id={}&ip_address={}'.format(
            region_id, ip_address
        )
        fake_devices.return_value = fake_resources.NETWORK_DEVICE_LIST1
        resp = self.get(path_query)
        device_resp = fake_resources.NETWORK_DEVICE_LIST1
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["ip_address"],
                         device_resp[0].ip_address)

        fake_devices.assert_called_once_with(
            mock.ANY, filters, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'network_devices_get_all')
    def test_get_network_devices_invalid_property(self, fake_devices):
        fake_devices.return_value = fake_resources.NETWORK_DEVICE_LIST2
        resp = self.get('/v1/network-devices?foo=isaninvalidproperty')
        self.assertEqual(len(resp.json), 2)
        fake_devices.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'network_devices_get_all')
    def test_get_network_devices(self, fake_devices):
        fake_devices.return_value = fake_resources.NETWORK_DEVICE_LIST2
        resp = self.get('/v1/network-devices')
        self.assertEqual(len(resp.json), 2)
        fake_devices.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'network_devices_get_all')
    def test_network_devices_get_by_region(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE_LIST1
        resp = self.get('/v1/network-devices?region_id=1')
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(
            resp.json[0]["hostname"],
            fake_resources.NETWORK_DEVICE_LIST1[0].hostname
        )

    @mock.patch.object(dbapi, 'network_devices_create')
    def test_create_network_devices_with_valid_data(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        data = {'hostname': 'NewNetDevice1', 'region_id': 1,
                'device_type': 'Sample', 'ip_address': '0.0.0.0'}
        resp = self.post('/v1/network-devices', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)

    @mock.patch.object(dbapi, 'network_devices_create')
    def test_create_netdevices_with_invalid_data(self, mock_devices):
        # data is missing entry
        data = {'hostname': 'Sample'}
        resp = self.post('/v1/network-devices', data=data)
        self.assertEqual(422, resp.status_code)
        mock_devices.assert_not_called()

    @mock.patch.object(dbapi, 'network_devices_create')
    def test_create_netdevices_with_invalid_property(self, mock_devices):
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        data = {'hostname': 'NetDevice1', 'region_id': 1,
                'device_type': 'Server', 'ip_address': '10.10.0.1',
                'foo': 'isinvalid'}
        resp = self.post('/v1/network-devices', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)
        mock_devices.assert_called_once()


class APIV1NetworkDevicesLabelsTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_devices_labels_update')
    def test_network_devices_labels_update(self, mock_devices):
        payload = {"labels": ["a", "b"]}
        mock_devices.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.put('v1/network-devices/1/labels', data=payload)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json, payload)

    @mock.patch.object(dbapi, 'network_devices_labels_update')
    def test_network_devices_labels_update_invalid_property(self, fake_device):
        fake_device.return_value = fake_resources.NETWORK_DEVICE1
        payload = {"foo": "isinvalid"}
        resp = self.put('v1/network-devices/1/labels', data=payload)
        self.assertEqual(resp.status_code, 200)
        fake_device.assert_called_once_with(mock.ANY, '1', {})

    @mock.patch.object(dbapi, 'network_devices_labels_delete')
    def test_network_devices_delete_labels(self, mock_network_device):
        payload = {"labels": ["label1", "label2"]}
        db_data = payload.copy()
        resp = self.delete('v1/network-devices/1/labels', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_network_device.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'network_devices_labels_delete')
    def test_network_devices_delete_bad_data_type(self, mock_network_device):
        payload = ["label1", "label2"]
        resp = self.delete('v1/network-devices/1/labels', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_network_device.assert_not_called()


class APIV1NetworkDevicesVariablesTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_devices_get_by_id')
    def test_network_devices_get_variables(self, mock_network_device):
        mock_network_device.return_value = fake_resources.NETWORK_DEVICE1
        resp = self.get('v1/network-devices/1/variables')
        expected = {"variables": {"key1": "value1", "key2": "value2"}}
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    @mock.patch.object(dbapi, 'network_devices_variables_update')
    def test_network_devices_put_variables(self, mock_network_device):
        db_return_value = copy.deepcopy(fake_resources.NETWORK_DEVICE1)
        db_return_value.variables["a"] = "b"
        mock_network_device.return_value = db_return_value
        payload = {"a": "b"}
        db_data = payload.copy()
        resp = self.put('v1/network-devices/1/variables', data=payload)
        self.assertEqual(resp.status_code, 200)
        mock_network_device.assert_called_once_with(mock.ANY, '1', db_data)
        expected = {
            "variables": {"key1": "value1", "key2": "value2", "a": "b"},
        }
        self.assertDictEqual(expected, resp.json)

    @mock.patch.object(dbapi, 'network_devices_variables_update')
    def test_network_devices_put_bad_data_type(self, mock_network_device):
        payload = ["a", "b"]
        resp = self.put('v1/network-devices/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_network_device.assert_not_called()

    @mock.patch.object(dbapi, 'network_devices_variables_delete')
    def test_network_devices_delete_variables(self, mock_network_device):
        payload = {"key1": "value1"}
        db_data = payload.copy()
        resp = self.delete('v1/network-devices/1/variables', data=payload)
        self.assertEqual(resp.status_code, 204)
        mock_network_device.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'network_devices_variables_delete')
    def test_network_devices_delete_bad_data_type(self, mock_network_device):
        payload = ["a", "b"]
        resp = self.delete('v1/network-devices/1/variables', data=payload)
        self.assertEqual(resp.status_code, 422)
        mock_network_device.assert_not_called()


class APIV1NetworkInterfacesTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_interfaces_get_all')
    def test_get_netinterfaces_by_ip_address_filter(self, fake_interfaces):
        device_id = 1
        ip_address = '10.10.0.1'
        filters = {'device_id': device_id, 'ip_address': ip_address}
        path_query = (
            '/v1/network-interfaces?device_id={}&ip_address={}'.format(
                device_id, ip_address
            )
        )
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE_LIST1
        resp = self.get(path_query)
        interface_resp = fake_resources.NETWORK_INTERFACE_LIST1
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json[0]["name"], interface_resp[0].name)

        fake_interfaces.assert_called_once_with(
            mock.ANY, filters, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'network_interfaces_get_all')
    def test_get_network_interfaces_by_device_id(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE_LIST1
        resp = self.get('/v1/network-interfaces?name=NetInterface&device_id=1')
        network_interface_resp = fake_resources.NETWORK_INTERFACE1
        self.assertEqual(resp.json[0]["name"], network_interface_resp.name)
        self.assertEqual(
            resp.json[0]['ip_address'], network_interface_resp.ip_address
        )

    @mock.patch.object(dbapi, 'network_interfaces_create')
    def test_network_interfaces_create_with_valid_data(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE1

        data = {'name': 'NewNetInterface', 'device_id': 1,
                'ip_address': '10.10.0.1', 'interface_type': 'interface_type1'}
        resp = self.post('/v1/network-interfaces', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertEqual(
            resp.json['ip_address'], data['ip_address']
        )
        self.assertIn("Location", resp.headers)

    @mock.patch.object(dbapi, 'network_interfaces_create')
    def test_network_interfaces_create_invalid_data(self, fake_interfaces):
        # data is missing entry
        data = {'name': 'sample'}
        resp = self.post('/v1/network-interfaces', data=data)
        self.assertEqual(422, resp.status_code)
        fake_interfaces.assert_not_called()

    @mock.patch.object(dbapi, 'network_interfaces_create')
    def test_network_interfaces_create_invalid_property(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK1
        data = {'name': 'PrivateNetwork', 'device_id': 1,
                'ip_address': '192.168.1.0', 'interface_type': 'Sample',
                'foo': 'isinvalid'}
        resp = self.post('/v1/network-interfaces', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)
        fake_interfaces.assert_called_once()

    @mock.patch.object(dbapi, 'network_interfaces_get_all')
    def test_get_network_interfaces(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE_LIST2
        resp = self.get('/v1/network-interfaces')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(resp.json), 2)
        fake_interfaces.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )

    @mock.patch.object(dbapi, 'network_interfaces_get_all')
    def test_get_network_interfaces_invalid_property(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE_LIST2
        resp = self.get('/v1/network-interfaces?foo=invalid')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(resp.json), 2)
        fake_interfaces.assert_called_once_with(
            mock.ANY, {}, {'limit': 30, 'marker': None},
        )


class APIV1NetworkInterfacesIDTest(APIV1Test):
    @mock.patch.object(dbapi, 'network_interfaces_get_by_id')
    def test_get_network_interfaces_by_id(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE1
        resp = self.get('/v1/network-interfaces/1')
        self.assertEqual(resp.json["name"],
                         fake_resources.NETWORK_INTERFACE1.name)
        self.assertEqual(
            resp.json['ip_address'],
            fake_resources.NETWORK_INTERFACE1.ip_address
        )

    @mock.patch.object(dbapi, 'network_interfaces_update')
    def test_network_interfaces_update(self, fake_interfaces):
        record = dict(fake_resources.NETWORK_INTERFACE1.items())
        payload = {'name': 'New'}
        db_data = payload.copy()
        record.update(payload)
        fake_interfaces.return_value = record

        resp = self.put('/v1/network-interfaces/1', data=payload)

        self.assertEqual(resp.json['name'], db_data['name'])
        self.assertEqual(200, resp.status_code)
        self.assertEqual(
            resp.json['ip_address'],
            fake_resources.NETWORK_INTERFACE1.ip_address
        )
        fake_interfaces.assert_called_once_with(mock.ANY, '1', db_data)

    @mock.patch.object(dbapi, 'network_interfaces_update')
    def test_network_interfaces_update_invalid_property(self, fake_interfaces):
        fake_interfaces.return_value = fake_resources.NETWORK_INTERFACE1
        payload = {'foo': 'invalid'}
        resp = self.put('/v1/network-interfaces/1', data=payload)

        self.assertEqual(200, resp.status_code)
        self.assertNotIn('foo', resp.json)
        fake_interfaces.assert_called_once_with(mock.ANY, '1', {})

    @mock.patch.object(dbapi, 'network_interfaces_delete')
    def test_network_interfaces_delete(self, fake_interfaces):
        resp = self.delete('/v1/network-interfaces/1')
        self.assertEqual(204, resp.status_code)
