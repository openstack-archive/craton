"""SQLAlchemy backend implementation."""

import sys
from collections import namedtuple

from oslo_config import cfg
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_log import log

import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound

from craton.inventory import exceptions
from craton.inventory.db.sqlalchemy import models


CONF = cfg.CONF

LOG = log.getLogger(__name__)


_FACADE = None

_DEFAULT_SQL_CONNECTION = 'sqlite://'
db_options.set_defaults(cfg.CONF,
                        connection=_DEFAULT_SQL_CONNECTION)


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = session.EngineFacade.from_config(cfg.CONF)
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def is_admin_context(context):
    """Check if this request had admin context."""
    # FIXME(sulo): fix after we have Users table
    return True


def require_admin_context(f):
    """Decorator that ensures admin request context."""

    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]):
            raise exceptions.AdminRequired()
        return f(*args, **kwargs)
    return wrapper


def model_query(context, model, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.
    :param context: context to query under
    :param model: model to query. Must be a subclass of ModelBase.
    :param session: if present, the session to use
    :param project_only: if present and context is user-type, then restrict
                         query to match the context's project_id.
    """
    session = kwargs.get('session') or get_session()
    project_only = kwargs.get('project_only')
    kwargs = dict()

    if project_only and not context.is_admin:
        kwargs['project_id'] = context.tenant

    return db_utils.model_query(
        model=model, session=session, args=args, **kwargs)


Blame = namedtuple('Blame', ['source', 'variable'])


def host_blame_variables(host, keys=None):
    """Determines the sources of how variables have been set for a host.
    :param host: host to get blame information
    :param keys: keys to check sourcing, or all keys if None

    Returns the (source, variable) in a named tuple; note that
    variable contains certain audit/governance information
    (created_at, modified_at).

    TODO(jimbaker) further extend schema on mixed-in variable tables
    to capture additional governance, such as user who set the key;
    this will then transparently become available in the blame.
    """
    if keys is None:
        keys = host.resolved.keys()
    sources = [host] + list(host._labels) + [host.region, host.cell]
    blamed = {}
    for key in keys:
        for source in sources:
            try:
                blamed[key] = Blame(source, source._variables[key])
                break
            except KeyError:
                pass
    return blamed


###################
# TODO(sulo): add filter on project_id and deleted fields

def cells_get_all(context, region):
    """Get all cells."""
    query = model_query(context, models.Cell, project_only=True)
    if region is not None:
        query = query.filter_by(region=region)

    try:
        result = query.all()
        return result
    except sqlalchemy.orm.exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


def cells_get_by_name(context, region, cell):
    """Get cell details given for a given cell in a region."""
    try:
        query = model_query(context, models.Cell).\
            filter_by(region_id=region).\
            filter_by(id=cell)
        return query.one()
    except sqlalchemy.orm.exc.NoResultFound:
        raise exceptions.NotFound()


def cells_create(context, values):
    """Create a new cell."""
    session = get_session()
    cell = models.Cell()
    with session.begin():
        cell.update(values)
        cell.save(session)
    return cell


def cells_update(context, cell_id, values):
    """Update an existing cell."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cell, session=session,
                            project_only=True)
        query = query.filter_by(id=cell_id)
        try:
            cell_ref = query.with_lockmode('update').one()
        except Exception:
            raise

        cell_ref.update(values)
        cell_ref.save(session)
    return cell_ref


def cells_delete(context, cell_id):
    """Delete an existing cell."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cell, session=session,
                            project_only=True)
        query = query.filter_by(id=cell_id)
        query.delete()


def cells_data_update(context, cell_id, data):
    """Update existing cells variables or create when
    its not present.
    """
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cell, session=session,
                            project_only=True)
        query = query.filter_by(id=cell_id)

        try:
            cell_ref = query.with_lockmode('update').one()
        except NoResultFound:
            # cell does not exist so cant do this
            raise

        for key in data:
            cell_ref.variables[key] = data[key]

    return cell_ref


def cells_data_delete(context, cell_id, data):
    """Delete the existing key (variable) from cells data."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cell, session=session,
                            project_only=True)
        query = query.filter_by(id=cell_id)

        try:
            cell_ref = query.with_lockmode('update').one()
        except NoResultFound:
            # cell does not exist so can't do this
            raise

        for key in data:
            try:
                del cell_ref.variables[data[key]]
            except KeyError:
                # This key does not exist so just ignore
                pass

    return cell_ref


def regions_get_all(context):
    """Get all available regions."""
    query = model_query(context, models.Region, project_only=True)
    result = query.all()
    return result


def regions_get_by_name(context, name):
    """Get cell detail for the region with given name."""
    query = model_query(context, models.Region, project_only=True)
    query = query.filter_by(name=name)
    return query.one()


def regions_get_by_id(context, region_id):
    """Get cell detail for the region with given id."""
    query = model_query(context, models.Region, project_only=True)
    query = query.filter_by(id=region_id)
    return query.one()


def regions_create(context, values):
    """Create a new region."""
    session = get_session()
    region = models.Region()
    with session.begin():
        region.update(values)
        region.save(session)
    return region


def regions_update(context, region_id, values):
    """Update an existing region."""
    # We dont have anything to update right now
    pass


def regions_delete(context, region_id):
    """Delete an existing region."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)
        query.delete()
    return


def regions_data_update(context, region_id, data):
    """
    Update existing region variables or create when its not present.
    """
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)

        try:
            region_ref = query.with_lockmode('update').one()
        except NoResultFound:
            # region does not exist so cant do this
            raise

        for key in data:
            region_ref.variables[key] = data[key]

    return region_ref


def regions_data_delete(context, region_id, data):
    """Delete the existing key (variable) from region data."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)

        try:
            region_ref = query.with_lockmode('update').one()
        except NoResultFound:
            # region does not exist so cant do this
            raise

        for key in data:
            try:
                del region_ref.variables[data[key]]
            except KeyError:
                # This key does not exist so just ignore
                pass

    return region_ref
