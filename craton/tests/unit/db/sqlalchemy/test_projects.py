from craton.db.sqlalchemy import api as dbapi
from craton.tests.unit.db import base


class TestProjectsGetAll(base.DBTestCase):

    def test_link_params_dictionary(self):
        _, links = dbapi.projects_get_all(
            self.context,
            filters={'name': None, 'id': None,
                     'sort_keys': ['id', 'created_at'], 'sort_dir': 'asc'},
            pagination_params={'limit': 30, 'marker': None},
        )
        self.assertNotIn('name', links)
        self.assertNotIn('id', links)
