import alembic
import os
import uuid

from alembic import config as alembic_config
import alembic.migration as alembic_migration
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from oslo_db.sqlalchemy import enginefacade

from craton.api.v1.resources import utils
from craton.db.sqlalchemy import models


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


def create_bootstrap_project(name, project_id=None, db_uri=None):
    """Creates a new project.
    :param name: Name of the new project
    """
    if not project_id:
        project_id = str(uuid.uuid4())
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    project = models.Project(name=name,
                             id=project_id)

    try:
        project = session.query(models.Project).filter_by(name=name).one()
    except sa_exc.NoResultFound:
        session.add(project)
        session.commit()

    return project


def create_bootstrap_user(project_id, username, db_uri=None):
    """Creates a new project.
    :param username: Username for new user
    :param project_id: Project ID for the user
    """
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    api_key = utils.gen_api_key()

    user = models.User(project_id=project_id,
                       username=username,
                       api_key=api_key,
                       is_admin=True,
                       is_root=True)
    try:
        session.add(user)
        session.commit()
    except exc.IntegrityError as err:
        if err.orig.args[0] == 1062:
            # NOTE(sulo): 1062 is the normal sql duplicate error code
            # also see pymysql/constants/ER.py#L65
            session.rollback()
            user = session.query(models.User).filter_by(username=username)
            user = user.filter_by(project_id=project_id).one()
            return user
        else:
            raise

    return user
