import copy
import uuid

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base

default_pagination = {'limit': 30, 'marker': None}

project1 = {'name': 'project1'}
project2 = {'name': 'project2'}


class ProjectsDBTestCase(base.DBTestCase):

    def test_create_project(self):
        # Set root, as only admin project can create other projects
        project = dbapi.projects_create(self.context, project1)
        self.assertEqual(project['name'], project1['name'])

    def test_create_project_no_root_fails(self):
        context = copy.deepcopy(self.context)
        context.is_admin_project = False
        self.assertRaises(exceptions.AdminRequired,
                          dbapi.projects_create,
                          context,
                          project1)

    def test_project_get_all(self):
        dbapi.projects_create(self.context, project1)
        dbapi.projects_create(self.context, project2)

        res = dbapi.projects_get_all(self.context, {}, default_pagination)
        self.assertEqual(len(res), 2)

    def test_project_get_no_admin_project_raises(self):
        dbapi.projects_create(self.context, project1)
        dbapi.projects_create(self.context, project2)

        # Now set admin_project = false to become normal project user
        context = copy.deepcopy(self.context)
        context.is_admin_project = False
        self.assertRaises(exceptions.AdminRequired,
                          dbapi.projects_get_all,
                          context,
                          {}, default_pagination)

    def test_project_get_by_id(self):
        project = dbapi.projects_create(self.context, project1)
        res = dbapi.projects_get_by_id(self.context, project['id'])
        self.assertEqual(str(res['id']), str(project['id']))

    def test_project_create_id_uuid_type(self):
        project = dbapi.projects_create(self.context, project1)
        self.assertEqual(type(project['id']), uuid.UUID)

    def test_project_get_id_uuid_type(self):
        project = dbapi.projects_create(self.context, project1)
        res = dbapi.projects_get_by_id(self.context, project['id'])
        self.assertEqual(type(res['id']), uuid.UUID)

    def test_project_variables_update_does_update_variables(self):
        create_res = dbapi.projects_create(self.context, project1)
        res = dbapi.projects_get_by_id(self.context, create_res.id)
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.variables_update_by_resource_id(
            self.context, "projects", res.id, variables
        )
        self.assertEqual(res.variables, variables)
        new_variables = {"key1": "tom", "key2": "cat"}
        res = dbapi.variables_update_by_resource_id(
            self.context, "projects", res.id, new_variables
        )
        self.assertEqual(res.variables, new_variables)

    def test_project_variables_delete(self):
        create_res = dbapi.projects_create(self.context, project1)
        res = dbapi.projects_get_by_id(self.context, create_res.id)
        self.assertEqual(res.variables, {})
        variables = {"key1": "value1", "key2": "value2"}
        res = dbapi.variables_update_by_resource_id(
            self.context, "projects", res.id, variables
        )
        self.assertEqual(res.variables, variables)
        # NOTE(sulo): we delete variables by their key
        res = dbapi.variables_delete_by_resource_id(
            self.context, "projects", res.id, {"key1": "key1"}
        )
        self.assertEqual(res.variables, {"key2": "value2"})
