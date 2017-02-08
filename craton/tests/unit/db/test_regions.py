import uuid

from craton.db import api as dbapi
from craton.tests.unit.db import base
from craton import exceptions

default_pagination = {'limit': 30, 'marker': None}

project_id1 = uuid.uuid4().hex
cloud_id1 = uuid.uuid4().hex
region1 = {'project_id': project_id1, 'cloud_id': cloud_id1, 'name': 'region1'}


class RegionsDBTestCase(base.DBTestCase):

    def test_region_create(self):
        try:
            dbapi.regions_create(self.context, region1)
        except Exception:
            self.fail("Region create raised unexpected exception")

    def test_region_create_duplicate_name_raises(self):
        dbapi.regions_create(self.context, region1)
        self.assertRaises(exceptions.DuplicateRegion, dbapi.regions_create,
                          self.context, region1)

    def test_regions_get_all(self):
        dbapi.regions_create(self.context, region1)
        filters = {}
        res, _ = dbapi.regions_get_all(self.context, filters,
                                       default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'region1')

    def test_regions_get_all_with_var_filters(self):
        res = dbapi.regions_create(self.context, region1)
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.variables_update_by_resource_id(
            self.context, "regions", res.id, variables
        )
        filters = {}
        filters["vars"] = "key1:value1"
        regions, _ = dbapi.regions_get_all(
            self.context, filters, default_pagination,
        )
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0].name, region1['name'])

    def test_regions_get_all_with_var_filters_noexist(self):
        res = dbapi.regions_create(self.context, region1)
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.variables_update_by_resource_id(
            self.context, "regions", res.id, variables
        )
        filters = {}
        filters["vars"] = "key1:value12"
        regions, _ = dbapi.regions_get_all(
            self.context, filters, default_pagination,
        )
        self.assertEqual(len(regions), 0)

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
        dbapi.regions_create(self.context, region1)
        res = dbapi.regions_get_by_id(self.context, 1)
        self.assertEqual(res.name, 'region1')
        new_name = "region_New1"
        res = dbapi.regions_update(self.context, res.id,
                                   {'name': 'region_New1'})
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
