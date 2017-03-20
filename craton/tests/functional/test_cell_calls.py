from craton.tests.functional.test_variable_calls import \
    APIV1ResourceWithVariablesTestCase


class APIV1CellTest(APIV1ResourceWithVariablesTestCase):

    resource = 'cells'

    def setUp(self):
        super(APIV1CellTest, self).setUp()
        self.cloud = self.create_cloud()
        self.region = self.create_region()

    def tearDown(self):
        super(APIV1CellTest, self).tearDown()

    def create_cloud(self):
        return super(APIV1CellTest, self).create_cloud(name='cloud-1')

    def create_region(self):
        return super(APIV1CellTest, self).create_region(
            name='region-1',
            cloud=self.cloud,
            variables={"region": "one"},
        )

    def create_cell(self, name, variables=None):
        return super(APIV1CellTest, self).create_cell(
            name=name,
            cloud=self.cloud,
            region=self.region,
            variables=variables
        )

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
        payload = {'name': 'test-cell', 'region_id': self.region['id'],
                   "cloud_id": self.cloud['id']}
        cell = self.post(url, data=payload)
        self.assertEqual(409, cell.status_code)

    def test_cell_create_with_extra_id_property_fails(self):
        url = self.url + '/v1/cells'
        payload = {'region_id': self.region['id'],
                   'cloud_id': self.cloud['id'], 'name': 'a', 'id': 3}
        cell = self.post(url, data=payload)
        self.assertEqual(400, cell.status_code)
        msg = (
            "The request included the following errors:\n"
            "- Additional properties are not allowed ('id' was unexpected)"
        )
        self.assertEqual(cell.json()['message'], msg)

    def test_cell_create_with_extra_created_at_property_fails(self):
        url = self.url + '/v1/cells'
        payload = {'region_id': self.region['id'],
                   'cloud_id': self.cloud['id'], 'name': 'a',
                   'created_at': "some date"}
        cell = self.post(url, data=payload)
        self.assertEqual(400, cell.status_code)
        msg = (
            "The request included the following errors:\n"
            "- Additional properties are not allowed "
            "('created_at' was unexpected)"
        )
        self.assertEqual(cell.json()['message'], msg)

    def test_cell_create_with_extra_updated_at_property_fails(self):
        url = self.url + '/v1/cells'
        payload = {'region_id': self.region['id'],
                   'cloud_id': self.cloud['id'], 'name': 'a',
                   'updated_at': "some date"}
        cell = self.post(url, data=payload)
        self.assertEqual(400, cell.status_code)
        msg = (
            "The request included the following errors:\n"
            "- Additional properties are not allowed "
            "('updated_at' was unexpected)"
        )
        self.assertEqual(cell.json()['message'], msg)

    def test_cells_get_all_with_details(self):
        self.create_cell('cell1', variables={'a': 'b'})
        self.create_cell('cell2', variables={'c': 'd'})
        url = self.url + '/v1/cells?details=all'
        resp = self.get(url)
        cells = resp.json()['cells']
        self.assertEqual(2, len(cells))
        for cell in cells:
            self.assertTrue('variables' in cell)

        for cell in cells:
            if cell['name'] == 'cell1':
                expected = {'a': 'b', "region": "one"}
                self.assertEqual(expected, cell['variables'])
            if cell['name'] == 'cell2':
                expected = {'c': 'd', "region": "one"}
                self.assertEqual(expected, cell['variables'])

    def test_cells_get_all_for_region(self):
        # Create a cell first
        self.create_cell('cell-1')
        url = self.url + '/v1/cells?region_id={}'.format(self.region['id'])
        resp = self.get(url)
        cells = resp.json()['cells']
        self.assertEqual(1, len(cells))
        self.assertEqual(['cell-1'], [i['name'] for i in cells])

    def test_cells_get_all_for_cloud(self):
        # Create a cell first
        for i in range(2):
            self.create_cell('cell-{}'.format(str(i)))
        url = self.url + '/v1/cells?cloud_id={}'.format(self.cloud['id'])
        resp = self.get(url)
        cells = resp.json()['cells']
        self.assertEqual(2, len(cells))
        self.assertEqual(['cell-0', 'cell-1'], [i['name'] for i in cells])

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

    def test_get_cell_resolved_vars(self):
        cellvars = {"who": "that"}
        cell = self.create_cell('cell1', variables=cellvars)
        url = self.url + '/v1/cells/{}'.format(cell['id'])
        resp = self.get(url)
        cell_with_detail = resp.json()
        self.assertEqual('cell1', cell_with_detail['name'])
        self.assertEqual({"who": "that", "region": "one"},
                         cell_with_detail['variables'])

    def test_get_cell_unresolved_vars(self):
        cellvars = {"who": "that"}
        cell = self.create_cell('cell1', variables=cellvars)
        cell_id = cell['id']
        url = self.url + '/v1/cells/{}?resolved-values=false'.format(cell_id)
        resp = self.get(url)
        cell_with_detail = resp.json()
        self.assertEqual('cell1', cell_with_detail['name'])
        self.assertEqual({"who": "that"}, cell_with_detail['variables'])

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
