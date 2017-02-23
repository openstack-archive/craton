from craton.tests.functional.test_variable_calls import \
    APIV1ResourceWithVariablesTestCase


class APIV1CellTest(APIV1ResourceWithVariablesTestCase):

    resource = 'cells'

    def setUp(self):
        super(APIV1CellTest, self).setUp()
        self.region = self.create_region()

    def tearDown(self):
        super(APIV1CellTest, self).tearDown()

    def create_region(self):
        url = self.url + '/v1/regions'
        payload = {'name': 'region-1'}
        region = self.post(url, data=payload)
        self.assertEqual(201, region.status_code)
        self.assertIn('Location', region.headers)
        self.assertEqual(
            region.headers['Location'],
            "{}/{}".format(url, region.json()['id'])
        )
        return region.json()

    def create_cell(self, name, variables=None):
        url = self.url + '/v1/cells'
        payload = {'name': name, 'region_id': self.region['id']}
        if variables:
            payload['variables'] = variables
        cell = self.post(url, data=payload)
        self.assertEqual(201, cell.status_code)
        self.assertIn('Location', cell.headers)
        self.assertEqual(
            cell.headers['Location'],
            "{}/{}".format(url, cell.json()['id'])
        )
        return cell.json()

    def test_cell_create_with_variables(self):
        variables = {'a': 'b'}
        cell = self.create_cell('cell-a', variables=variables)
        self.assertEqual('cell-a', cell['name'])
        self.assertEqual(variables, cell['variables'])

    def test_create_cell_supports_vars_ops(self):
        cell = self.create_cell('new-cell', {'a': 'b'})
        self.assert_vars_get_expected(cell['id'], {'a': 'b'})
        self.assert_vars_can_be_set(cell['id'])
        self.assert_vars_can_be_deleted(cell['id'])

    def test_cell_create_with_no_name_fails(self):
        url = self.url + '/v1/cells'
        payload = {'region_id': self.region['id']}
        cell = self.post(url, data=payload)
        self.assertEqual(400, cell.status_code)

    def test_cell_create_with_duplicate_name_fails(self):
        self.create_cell('test-cell')
        url = self.url + '/v1/cells'
        payload = {'name': 'test-cell', 'region_id': self.region['id']}
        cell = self.post(url, data=payload)
        self.assertEqual(409, cell.status_code)

    def test_cell_create_with_extra_property_fails(self):
        url = self.url + '/v1/cells'
        payload = {'region_id': self.region['id'], 'name': 'a', 'id': 3}
        cell = self.post(url, data=payload)
        self.assertEqual(400, cell.status_code)
        msg = ["Additional properties are not allowed ('id' was unexpected)"]
        self.assertEqual(resp.json()['errors'], msg)

    def test_cells_get_all_for_region(self):
        # Create a cell first
        self.create_cell('cell-1')
        url = self.url + '/v1/cells?region_id={}'.format(self.region['id'])
        resp = self.get(url)
        cells = resp.json()['cells']
        self.assertEqual(1, len(cells))
        self.assertEqual(['cell-1'], [i['name'] for i in cells])

    def test_cell_get_all_with_name_filter(self):
        self.create_cell('cell1')
        self.create_cell('cell2')
        url = self.url + '/v1/cells?name=cell2'
        resp = self.get(url)
        cells = resp.json()['cells']
        self.assertEqual(1, len(cells))
        self.assertEqual({'cell2'}, {cell['name'] for cell in cells})

    def test_get_cell_details(self):
        cellvars = {"who": "that"}
        cell = self.create_cell('cell1', variables=cellvars)
        url = self.url + '/v1/cells/{}'.format(cell['id'])
        resp = self.get(url)
        cell_with_detail = resp.json()
        self.assertEqual('cell1', cell_with_detail['name'])
        self.assertEqual(cellvars, cell_with_detail['variables'])

    def test_cell_update(self):
        cell = self.create_cell('cell-1')
        url = self.url + '/v1/cells/{}'.format(cell['id'])
        data = {'note': 'Updated cell note.'}
        resp = self.put(url, data=data)
        self.assertEqual(200, resp.status_code)
        cell = resp.json()
        self.assertEqual(data['note'], cell['note'])

    def test_cell_delete(self):
        cell1 = self.create_cell('cell-1')
        self.create_cell('cell-2')
        url = self.url + '/v1/cells'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        cells = resp.json()['cells']
        self.assertEqual(2, len(cells))
        self.assertEqual({'cell-1', 'cell-2'},
                         {cell['name'] for cell in cells})

        delurl = self.url + '/v1/cells/{}'.format(cell1['id'])
        resp = self.delete(delurl)
        self.assertEqual(204, resp.status_code)

        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        cells = resp.json()['cells']
        self.assertEqual(1, len(cells))
        self.assertEqual({'cell-2'},
                         {cell['name'] for cell in cells})
