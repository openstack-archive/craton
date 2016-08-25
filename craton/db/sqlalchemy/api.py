"""SQLAlchemy backend implementation."""

import sys
import six

from oslo_config import cfg
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_log import log

import sqlalchemy.orm.exc as sa_exc
from sqlalchemy.orm import with_polymorphic

from craton import exceptions
from craton.db.sqlalchemy import models


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
    """Check if this request had admin project context."""
    if (context.is_admin and context.is_admin_project):
        return True
    return False


def is_project_admin_context(context):
    """Check if this request has admin context with in the project."""
    if context.is_admin:
        return True
    return False


def require_admin_context(f):
    """Decorator that ensures admin request context."""
    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]):
            raise exceptions.AdminRequired()
        return f(*args, **kwargs)
    return wrapper


def require_project_admin_context(f):
    """Decorator that ensures admin or project_admin request context."""
    def wrapper(*args, **kwargs):
        if is_admin_context(args[0]):
            return f(*args, **kwargs)
        elif is_project_admin_context(args[0]):
            return f(*args, **kwargs)
        else:
            raise exceptions.AdminRequired()
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


def get_user_info(context, username):
    """Get user info."""
    query = model_query(context, models.User, project_only=True)
    query = query.filter_by(username=username)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


def cells_get_all(context, region, filters):
    """Get all cells."""
    query = model_query(context, models.Cell, project_only=True)
    if region is not None:
        query = query.filter_by(region_id=region)

    if "var_filters" in filters:
        query = query.join('variable_association', 'variables')
        for k, v in six.iteritems(filters["var_filters"]):
            query = query.filter_by(key=k).filter_by(value=v)

    try:
        return query.all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


def cells_get_by_name(context, region_id, cell_id):
    """Get cell details given for a given cell in a region."""
    try:
        query = model_query(context, models.Cell).\
            filter_by(region_id=region_id).\
            filter_by(name=cell_id)
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


def cells_get_by_id(context, cell_id):
    """Get cell details given for a given cell id."""
    try:
        query = model_query(context, models.Cell).\
            filter_by(id=cell_id)
        return query.one()
    except sa_exc.NoResultFound:
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
        except sa_exc.NoResultFound:
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
        except sa_exc.NoResultFound:
            # cell does not exist so cant do this
            raise

        for key in data:
            try:
                del cell_ref.variables[data[key]]
            except KeyError:
                # This key does not exist so just ignore
                pass

    return cell_ref


def regions_get_all(context, filters):
    """Get all available regions."""
    query = model_query(context, models.Region, project_only=True)

    if "var_filters" in filters:
        query = query.join('variable_association', 'variables')
        for k, v in six.iteritems(filters["var_filters"]):
            query = query.filter_by(key=k).filter_by(value=v)

    try:
        return query.all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


def regions_get_by_name(context, name):
    """Get cell detail for the region with given name."""
    query = model_query(context, models.Region, project_only=True)
    query = query.filter_by(name=name)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


def regions_get_by_id(context, region_id):
    """Get cell detail for the region with given id."""
    query = model_query(context, models.Region, project_only=True)
    query = query.filter_by(id=region_id)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


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
        except sa_exc.NoResultFound:
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
        except sa_exc.NoResultFound:
            # region does not exist so cant do this
            raise

        for key in data:
            try:
                del region_ref.variables[data[key]]
            except KeyError:
                # This key does not exist so just ignore
                pass

    return region_ref


def hosts_get_by_region(context, region_id, filters):
    """Get all hosts for this region.

    :param region_id: ID for the region
    :param filters: filters wich contains differnt keys/values to match.
    Supported filters are by name, ip_address, id and cell_id.
    """
    host_devices = with_polymorphic(models.Device, [models.Host])
    query = model_query(context, host_devices, project_only=True)
    query = query.filter_by(region_id=region_id)

    if "name" in filters:
        query = query.filter_by(name=filters["name"])
    if "ip_address" in filters:
        query = query.filter_by(ip_address=filters["ip_address"])
    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "cell" in filters:
        query = query.filter_by(cell_id=filters["cell"])
    if "device_type" in filters:
        query = query.filter_by(device_type=filters["device_type"])

    if "var_filters" in filters:
        query = query.join('variable_association', 'variables')
        for k, v in six.iteritems(filters["var_filters"]):
            query = query.filter_by(key=k).filter_by(value=v)

    try:
        result = query.all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)
    return result


def hosts_get_by_id(context, host_id):
    """Get details for the host with given id."""
    host_devices = with_polymorphic(models.Device, '*')
    query = model_query(context, host_devices, project_only=True).\
        filter_by(id=host_id)
    try:
        result = query.one()
        LOG.info("Result by host id %s" % result)
    except sa_exc.NoResultFound:
        LOG.error("No result found for host with id %s" % host_id)
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)
    return result


def hosts_create(context, values):
    """Create a new host."""
    session = get_session()
    host = models.Host()
    with session.begin():
        host.update(values)
        host.save(session)
    return host


def hosts_update(context, host_id, values):
    """Update an existing host."""
    return None


def hosts_delete(context, host_id):
    """Delete an existing host."""
    session = get_session()
    with session.begin():
        host_devices = with_polymorphic(models.Device, '*')
        query = model_query(context, host_devices, session=session,
                            project_only=True)
        query = query.filter_by(id=host_id)
        query.delete()
    return


def hosts_data_update(context, host_id, data):
    """
    Update existing host variables or create when its not present.
    """
    session = get_session()
    with session.begin():
        host_devices = with_polymorphic(models.Device, '*')
        query = model_query(context, host_devices, session=session,
                            project_only=True)
        query = query.filter_by(id=host_id)

        try:
            host_ref = query.with_lockmode('update').one()
        except sa_exc.NoResultFound:
            raise exceptions.NotFound()

        for key in data:
            host_ref.variables[key] = data[key]

    return host_ref


def hosts_data_delete(context, host_id, data):
    """Delete the existing key (variable) from region data."""
    session = get_session()
    with session.begin():
        host_devices = with_polymorphic(models.Device, '*')
        query = model_query(context, host_devices, session=session,
                            project_only=True)
        query = query.filter_by(id=host_id)

        try:
            host_ref = query.with_lockmode('update').one()
        except sa_exc.NoResultFound:
            raise exceptions.NotFound()

        for key in data:
            try:
                del host_ref.variables[data[key]]
            except KeyError:
                pass

    return host_ref


@require_admin_context
def projects_get_all(context):
    """Get all the projects."""
    query = model_query(context, models.Project)
    try:
        return query.all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


@require_admin_context
def projects_get_by_name(context, project_name):
    """Get all projects that match the given name."""
    query = model_query(context, models.Project)
    query = query.filter(models.Project.name.like(project_name))
    try:
        return query.all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


@require_admin_context
def projects_get_by_id(context, project_id):
    """Get project by its id."""
    query = model_query(context, models.Project)
    query = query.filter_by(id=project_id)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


@require_admin_context
def projects_create(context, values):
    """Create a new project with given values."""
    session = get_session()
    project = models.Project()
    with session.begin():
        project.update(values)
        project.save(session)
    return project


@require_admin_context
def projects_delete(context, project_id):
    """Delete an existing project given by its id."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Project, session=session)
        query = query.filter_by(id=project_id)
        query.delete()


@require_project_admin_context
def users_get_all(context):
    """Get all the users."""
    if is_admin_context(context):
        LOG.info("Getting all users as root user")
        query = model_query(context, models.User)
    else:
        LOG.info("Getting all users as project admin user")
        query = model_query(context, models.User, project_only=True)
        query = query.filter_by(project_id=context.tenant)

    return query.all()


@require_project_admin_context
def users_get_by_name(context, user_name):
    """Get all users that match the given username."""
    if is_admin_context(context):
        query = model_query(context, models.User)
    else:
        query = model_query(context, models.User, project_only=True)

    query = query.filter_by(username=user_name)
    return query.all()


@require_project_admin_context
def users_get_by_id(context, user_id):
    """Get user by its id."""
    if is_admin_context(context):
        query = model_query(context, models.User)
    else:
        query = model_query(context, models.User, project_only=True)

    query = query.filter_by(id=user_id)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


@require_project_admin_context
def users_create(context, values):
    """Create a new user with given values."""
    session = get_session()
    user = models.User()
    with session.begin():
        user.update(values)
        user.save(session)
    return user


@require_project_admin_context
def users_delete(context, user_id):
    """Delete an existing user given by its id."""
    LOG.info("Deleting user with id %s" % user_id)
    session = get_session()
    with session.begin():
        query = model_query(context, models.User, session=session)
        query = query.filter_by(id=user_id)
        query.delete()
    return
