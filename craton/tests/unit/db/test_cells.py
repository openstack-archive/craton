from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base


cell1 = {'region_id': 1, 'project_id': 1, 'name': 'cell1'}


class CellsDBTestCase(base.DBTestCase):

    def test_cells_create(self):
        try:
            dbapi.cells_create(self.context, cell1)
        except Exception:
            self.fail("Cell create raised unexpected exception")

    def test_cells_get_all(self):
        dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_all(self.context, cell1['region_id'])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'cell1')

    def test_cell_get_by_name(self):
        dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_name(self.context, cell1['region_id'],
                                      cell1['name'])
        self.assertEqual(res.name, 'cell1')

    def test_cell_get_by_name_no_exit_raises(self):
        self.assertRaises(exceptions.NotFound, dbapi.cells_get_by_name,
                          self.context, 'fake-region', 'fake-cell')

    def test_cell_delete(self):
        dbapi.cells_create(self.context, cell1)
        # First make sure we have the cell
        res = dbapi.cells_get_by_name(self.context, cell1['region_id'],
                                      cell1['name'])
        self.assertEqual(res.name, 'cell1')

        dbapi.cells_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound, dbapi.cells_get_by_name,
                          self.context, 'fake-region', 'fake-cell')

    def test_cell_data_update_does_create_variables(self):
        dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_name(self.context, cell1['region_id'],
                                      cell1['name'])
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.cells_data_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)

    def test_cell_update(self):
        dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_name(self.context, cell1['region_id'],
                                      cell1['name'])
        self.assertEqual(res.name, 'cell1')
        name = "cell1"
        res = dbapi.cells_update(self.context, res.id, {'name': 'cell1'})
        self.assertEqual(res.name, name)
        new_name = 'cell1_New'
        res = dbapi.cells_update(self.context, res.id, {'name': 'cell1_New'})
        self.assertEqual(res.name, new_name)

    def test_cell_data_update_does_update_variables(self):
        dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_name(self.context, cell1['region_id'],
                                      cell1['name'])
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.cells_data_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)
        new_variables = {"key1": "tom", "key2": "cat"}
        res = dbapi.cells_data_update(self.context, res.id, new_variables)
        self.assertEqual(res.variables, new_variables)

    def test_cell_data_delete(self):
        dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_name(self.context, cell1['region_id'],
                                      cell1['name'])
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.cells_data_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)
        # NOTE(sulo): we delete variables by their key
        res = dbapi.cells_data_delete(self.context, res.id, {"key1": "key1"})
        self.assertEqual(res.variables, {"key2": "value2"})
