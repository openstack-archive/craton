from craton.tests.functional import TestCase


class APIV1CellTest(TestCase):

    def setUp(self):
        super(APIV1CellTest, self).setUp()
        self.region = self.create_region()

    def tearDown(self):
        super(APIV1CellTest, self).tearDown()

    def create_region(self):
        url = self.url + '/v1/regions'
        payload = {'name': 'region-1'}
        region = self.post(url, data=payload)
        self.assertEqual(200, region.status_code)
        return region.json()

    def create_cell(self, name, variables=None):
        url = self.url + '/v1/cells'
        payload = {'name': name, 'region_id': self.region['id']}
        if variables:
            payload['variables'] = variables
        cell = self.post(url, data=payload)
        self.assertEqual(200, cell.status_code)
        return cell.json()

    def test_cell_create_with_variables(self):
        variables = {"a": "b"}
        cell = self.create_cell('cell-a', variables=variables)
        self.assertEqual('cell-a', cell['name'])
        self.assertEqual(variables, cell['variables'])

    def test_cell_create_with_no_name_fails(self):
        url = self.url + '/v1/cells'
        payload = {'region_id': self.region['id']}
        cell = self.post(url, data=payload)
        self.assertEqual(422, cell.status_code)

    def test_cell_create_with_duplicate_name_fails(self):
        self.create_cell('test-cell')
        url = self.url + '/v1/cells'
        payload = {'name': 'test-cell', 'region_id': self.region['id']}
        cell = self.post(url, data=payload)
        self.assertEqual(409, cell.status_code)

    def test_cells_get_all_for_region(self):
        # Create a cell first
        self.create_cell('cell-1')
        url = self.url + '/v1/cells?region_id={}'.format(self.region['id'])
        cells = self.get(url)
        self.assertEqual(1, len(cells.json()))
        self.assertEqual(['cell-1'], [i['name'] for i in cells.json()])

    def test_cell_get_all_with_name_filter(self):
        self.create_cell('cell1')
        self.create_cell('cell2')
        url = self.url + '/v1/cells?name=cell2'
        cell = self.get(url)
        self.assertEqual(1, len(cell.json()))

    def test_get_cell_details(self):
        cellvars = {"who":"that"}
        cell = self.create_cell('cell1', variables=cellvars)
        url = self.url + '/v1/cells/{}'.format(cell['id'])
        cell_with_detail = self.get(url)
        self.assertEqual('cell1', cell_with_detail.json()['name'])
        self.assertEqual(cellvars, cell_with_detail.json()['variables'])

    def test_cell_update(self):
        cell = self.create_cell('cell-1')
        url = self.url + '/v1/cells/{}'.format(cell['id'])
        data = {'note': 'Updated cell note.'}
        cell = self.put(url, data=data)
        self.assertEqual(data['note'], cell.json()['note'])

    def test_cell_delete(self):
        cell1 = self.create_cell('cell-1')
        cell2 = self.create_cell('cell-2')
        url = self.url + '/v1/cells'
        cells = self.get(url)
        self.assertEqual(2, len(cells.json()))

        delurl = self.url + '/v1/cells/{}'.format(cell1['id'])
        self.delete(delurl)

        cells = self.get(url)
        self.assertEqual(1, len(cells.json()))
