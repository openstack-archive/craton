import os

import alembic
from alembic import config as alembic_config
import alembic.migration as alembic_migration
from oslo_db.sqlalchemy import enginefacade


def _alembic_config():
    path = os.path.join(os.path.dirname(__file__), 'alembic.ini')
    config = alembic_config.Config(path)
    return config


def version(config=None, engine=None):
    """Current database version."""
    if engine is None:
        engine = enginefacade.get_legacy_facade().get_engine()
    with engine.connect() as conn:
        context = alembic_migration.MigrationContext.configure(conn)
        return context.get_current_revision()


def upgrade(revision, config=None):
    """Used for upgrading database.
    :param version: Desired database version
    """
    revision = revision or 'head'
    config = config or _alembic_config()

    alembic.command.upgrade(config, revision or 'head')


def stamp(revision, config=None):
    """Stamps database with provided revision.
    Don't run any migrations.
    :param revision: Should match one from repository or head - to stamp
                     database with most recent revision
    """
    config = config or _alembic_config()
    return alembic.command.stamp(config, revision=revision)


def revision(message=None, autogenerate=False, config=None):
    """Creates template for migration.
    :param message: Text that will be used for migration title
    :param autogenerate: If True - generates diff based on current database
                         state
    """
    config = config or _alembic_config()
    return alembic.command.revision(config, message=message,
                                    autogenerate=autogenerate)
