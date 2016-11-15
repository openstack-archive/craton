from craton.tests.functional import TestCase


class APIV1CellTest(TestCase):

    def setUp(self):
        super(APIV1CellTest, self).setUp()

    def test_cells_get_all_for_region_1(self):
        url = self.url + '/v1/cells?region_id=1'
        cells = self.get(url)
        self.assertEqual(len(cells.json()), 2)
        self.assertEqual(['C0001', 'C0002'], [i['name'] for i in cells.json()])

    def test_cells_get_details_for_cell_1(self):
        url = self.url + '/v1/cells/1'
        resp = self.get(url)
        cell = resp.json()
        self.assertEqual('C0001', cell['name'])
