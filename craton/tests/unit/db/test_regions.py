from craton.db import api as dbapi
from craton.tests.unit.db import base
from craton import exceptions


region1 = {'project_id': 1, 'name': 'region1'}


class RegionsDBTestCase(base.DBTestCase):

    def test_region_create(self):
        try:
            dbapi.regions_create(self.context, region1)
        except Exception:
            self.fail("Region create raised unexpected exception")

    def test_regions_get_all(self):
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_all(self.context)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'region1')

    def test_region_get_by_name(self):
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_by_name(self.context, region1['name'])
        self.assertEqual(res.name, 'region1')

    def test_region_get_by_id(self):
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_by_id(self.context, 1)
        self.assertEqual(res.name, 'region1')

    def test_region_get_by_name_no_exit_raises(self):
        # TODO(sulo): fix sqlalchemy api first
        pass

    def test_region_get_by_id_no_exist_raises(self):
        # TODO(sulo): fix sqlalchemy api first
        pass

    def test_region_update(self):
        dbapi.regions_update(self.context, region1)
        res = dbapi.regions_get_by_id(self.context, 1)
        self.assertEqual(res.name, {})
        name = "region1"
        res = dbapi.regions_update(self.context, res.id, name)
        self.assertEqual(res.name, name)
        new_name = "region_New1"
        res = dbapi.regions_update(self.context, res.id, new_name)
        self.assertEqual(res.name, new_name)

    def test_region_delete(self):
        dbapi.regions_create(self.context, region1)
        # First make sure we have the region
        res = dbapi.regions_get_by_name(self.context, region1['name'])
        self.assertEqual(res.name, 'region1')

        dbapi.regions_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound,
                          dbapi.regions_get_by_name,
                          self.context, 'fake-region')

    def test_region_data_update_does_create_variables(self):
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_by_name(self.context, region1['name'])
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.regions_data_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)

    def test_region_data_update_does_update_variables(self):
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_by_name(self.context, region1['name'])
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.regions_data_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)
        new_variables = {"key1": "tom", "key2": "cat"}
        res = dbapi.regions_data_update(self.context, res.id, new_variables)
        self.assertEqual(res.variables, new_variables)

    def test_region_data_delete(self):
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_by_name(self.context, region1['name'])
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.regions_data_update(self.context, res.id, variables)
        self.assertEqual(res.variables, variables)
        # NOTE(sulo): we delete variables by their key
        res = dbapi.regions_data_delete(self.context, res.id, {"key1": "key1"})
        self.assertEqual(res.variables, {"key2": "value2"})
