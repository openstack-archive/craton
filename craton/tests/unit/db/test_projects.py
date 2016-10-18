from oslo_utils import uuidutils

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base


project1 = {'name': 'project1'}
project2 = {'name': 'project2'}


class ProjectsDBTestCase(base.DBTestCase):

    def test_create_project(self):
        # Set root, as only admin project can create other projects
        self.context.is_admin_project = True
        project = dbapi.projects_create(self.context, project1)
        self.assertTrue(uuidutils.is_uuid_like(project['id']))
        self.assertEqual(project['name'], project1['name'])

    def test_create_project_no_root_fails(self):
        self.assertRaises(exceptions.AdminRequired,
                          dbapi.projects_create,
                          self.context,
                          project1)

    def test_project_get_all(self):
        self.context.is_admin_project = True
        dbapi.projects_create(self.context, project1)
        dbapi.projects_create(self.context, project2)

        res = dbapi.projects_get_all(self.context)
        self.assertEqual(len(res), 2)

    def test_project_get_no_admin_project_raises(self):
        self.context.is_admin_project = True
        dbapi.projects_create(self.context, project1)
        dbapi.projects_create(self.context, project2)

        # Now set admin_project = false to become normal project user
        self.context.is_admin_project = False
        self.assertRaises(exceptions.AdminRequired,
                          dbapi.projects_get_all,
                          self.context)

    def test_project_get_by_id(self):
        self.context.is_admin_project = True
        project = dbapi.projects_create(self.context, project1)
        res = dbapi.projects_get_by_id(self.context, project['id'])
        self.assertEqual(str(res['id']), project['id'])
