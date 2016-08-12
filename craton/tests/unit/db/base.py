import fixtures

from craton.db.sqlalchemy import api as sa_api
from craton.db.sqlalchemy import models
from craton.tests import TestCase


_DB_SCHEMA = None


class Database(fixtures.Fixture):
    def __init__(self):
        self.engine = sa_api.get_engine()
        self.engine.dispose()
        conn = self.engine.connect()
        self.setup_sqlite()
        self._DB = "".join(line for line in conn.connection.iterdump())
        self.engine.dispose()

    def setup_sqlite(self):
        # NOTE(sulo): there is no version here. We will be using
        # Alembic in the near future to manage migrations.
        models.Base.metadata.create_all(self.engine)

    def _setUp(self):
        conn = self.engine.connect()
        conn.connection.executescript(self._DB)
        self.addCleanup(self.engine.dispose)


class DBTestCase(TestCase):

    def setUp(self):
        super(DBTestCase, self).setUp()
        global _DB_SCHEMA
        if not _DB_SCHEMA:
            _DB_SCHEMA = Database()
        self.useFixture(_DB_SCHEMA)
