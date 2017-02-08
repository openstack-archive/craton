import uuid

from craton.db import api as dbapi
from craton.tests.unit.db import base
from craton import exceptions

default_pagination = {'limit': 30, 'marker': None}

project_id1 = uuid.uuid4().hex
cloud1 = {'project_id': project_id1, 'name': 'cloud1'}


class CloudsDBTestCase(base.DBTestCase):

    def test_cloud_create(self):
        try:
            dbapi.clouds_create(self.context, cloud1)
        except Exception:
            self.fail("Cloud create raised unexpected exception")

    def test_cloud_create_duplicate_name_raises(self):
        dbapi.clouds_create(self.context, cloud1)
        self.assertRaises(exceptions.DuplicateCloud, dbapi.clouds_create,
                          self.context, cloud1)

    def test_clouds_get_all(self):
        dbapi.clouds_create(self.context, cloud1)
        filters = {}
        res, _ = dbapi.clouds_get_all(self.context, filters,
                                      default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'cloud1')

    def test_clouds_get_all_with_var_filters(self):
        res = dbapi.clouds_create(self.context, cloud1)
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.variables_update_by_resource_id(
            self.context, "clouds", res.id, variables
        )
        filters = {}
        filters["vars"] = "key1:value1"
        clouds, _ = dbapi.clouds_get_all(
            self.context, filters, default_pagination,
        )
        self.assertEqual(len(clouds), 1)
        self.assertEqual(clouds[0].name, cloud1['name'])

    def test_clouds_get_all_with_var_filters_noexist(self):
        res = dbapi.clouds_create(self.context, cloud1)
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.variables_update_by_resource_id(
            self.context, "clouds", res.id, variables
        )
        filters = {}
        filters["vars"] = "key1:value12"
        clouds, _ = dbapi.clouds_get_all(
            self.context, filters, default_pagination,
        )
        self.assertEqual(len(clouds), 0)

    def test_cloud_get_by_name(self):
        dbapi.clouds_create(self.context, cloud1)
        res = dbapi.clouds_get_by_name(self.context, cloud1['name'])
        self.assertEqual(res.name, 'cloud1')

    def test_cloud_get_by_id(self):
        dbapi.clouds_create(self.context, cloud1)
        res = dbapi.clouds_get_by_id(self.context, 1)
        self.assertEqual(res.name, 'cloud1')

    def test_cloud_update(self):
        dbapi.clouds_create(self.context, cloud1)
        res = dbapi.clouds_get_by_id(self.context, 1)
        self.assertEqual(res.name, 'cloud1')
        new_name = "cloud_New1"
        res = dbapi.clouds_update(self.context, res.id,
                                  {'name': 'cloud_New1'})
        self.assertEqual(res.name, new_name)

    def test_cloud_delete(self):
        dbapi.clouds_create(self.context, cloud1)
        # First make sure we have the cloud
        res = dbapi.clouds_get_by_name(self.context, cloud1['name'])
        self.assertEqual(res.name, 'cloud1')

        dbapi.clouds_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound,
                          dbapi.clouds_get_by_name,
                          self.context, 'fake-cloud')
