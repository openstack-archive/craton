import uuid

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base

project_id1 = uuid.uuid4().hex

cell1 = {'region_id': 1, 'project_id': project_id1, 'name': 'cell1'}
cell1_region2 = {'region_id': 2, 'project_id': project_id1, 'name': 'cell1'}
cell2 = {'region_id': 1, 'project_id': project_id1, 'name': 'cell2'}

cells = (cell1, cell1_region2, cell2)
default_pagination = {'limit': 30, 'marker': None}


class CellsDBTestCase(base.DBTestCase):

    def test_cells_create(self):
        try:
            dbapi.cells_create(self.context, cell1)
        except Exception:
            self.fail("Cell create raised unexpected exception")

    def test_duplicate_cell_create_raises_409(self):
        dbapi.cells_create(self.context, cell1)
        self.assertRaises(exceptions.DuplicateCell, dbapi.cells_create,
                          self.context, cell1)

    def test_cells_get_all(self):
        dbapi.cells_create(self.context, cell1)
        filters = {
            "region_id": cell1["region_id"],
        }
        res, _ = dbapi.cells_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'cell1')

    def test_cells_get_all_filter_name(self):
        for cell in cells:
            dbapi.cells_create(self.context, cell)
        setup_res, _ = dbapi.cells_get_all(self.context, {},
                                           default_pagination)
        self.assertGreater(len(setup_res), 2)

        filters = {
            "name": cell1["name"],
        }
        res, _ = dbapi.cells_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 2)
        for cell in res:
            self.assertEqual(cell['name'], 'cell1')

    def test_cells_get_all_filter_id(self):
        for cell in cells:
            dbapi.cells_create(self.context, cell)
        setup_res, _ = dbapi.cells_get_all(self.context, {},
                                           default_pagination)
        self.assertGreater(len(setup_res), 2)
        self.assertEqual(
            len([cell for cell in setup_res if cell['id'] == 1]), 1
        )

        filters = {
            "id": 1,
        }
        res, _ = dbapi.cells_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['id'], 1)

    def test_cells_get_all_with_filters(self):
        res = dbapi.cells_create(self.context, cell1)
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.cells_variables_update(self.context, res.id, variables)
        filters = {
            "vars": "key2:value2",
            "region_id": cell1["region_id"],
        }
        res, _ = dbapi.cells_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'cell1')

    def test_cells_get_all_with_filters_noexist(self):
        res = dbapi.cells_create(self.context, cell1)
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.cells_variables_update(self.context, res.id, variables)
        filters = {}
        filters["vars"] = "key2:value5"
        res, _ = dbapi.cells_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 0)

    def test_cell_delete(self):
        create_res = dbapi.cells_create(self.context, cell1)
        # First make sure we have the cell
        res = dbapi.cells_get_by_id(self.context, create_res.id)
        self.assertEqual(res.name, 'cell1')

        dbapi.cells_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound, dbapi.cells_get_by_id,
                          self.context, res.id)

    def test_cell_variables_update_does_create_variables(self):
        create_res = dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_id(self.context, create_res.id)
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.cells_variables_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)

    def test_cell_update(self):
        create_res = dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_id(self.context, create_res.id)
        self.assertEqual(res.name, 'cell1')
        new_name = 'cell1_New'
        res = dbapi.cells_update(self.context, res.id, {'name': 'cell1_New'})
        self.assertEqual(res.name, new_name)

    def test_cell_variables_update_does_update_variables(self):
        create_res = dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_id(self.context, create_res.id)
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.cells_variables_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)
        new_variables = {"key1": "tom", "key2": "cat"}
        res = dbapi.cells_variables_update(self.context, res.id, new_variables)
        self.assertEqual(res.variables, new_variables)

    def test_cell_variables_delete(self):
        create_res = dbapi.cells_create(self.context, cell1)
        res = dbapi.cells_get_by_id(self.context, create_res.id)
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.cells_variables_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)
        # NOTE(sulo): we delete variables by their key
        res = dbapi.cells_variables_delete(self.context, res.id,
                                           {"key1": "key1"})
        self.assertEqual(res.variables, {"key2": "value2"})
