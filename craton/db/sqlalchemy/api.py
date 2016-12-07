"""SQLAlchemy backend implementation."""

import sys

from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_log import log
from oslo_utils import uuidutils

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


def add_var_filters_to_query(query, filters):
    # vars filters are of form ?vars=a:b,c:d
    var_filters = filters['vars'].split(',')
    for filters in var_filters:
        k, v = filters.split(':', 1)
        query = query.filter(models.Variable.key == k)
        query = query.filter(models.Variable.value == v)

    return query


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


def _device_labels_update(context, device_type, device_id, labels):
    """Update labels for the given device. Add the label if it is not present
    in host labels list, otherwise do nothing."""
    session = get_session()
    with session.begin():
        devices = with_polymorphic(models.Device, '*')
        query = model_query(context, devices, session=session,
                            project_only=True)
        query = query.filter_by(type=device_type)
        query = query.filter_by(id=device_id)
        try:
            device = query.one()
        except sa_exc.NoResultFound:
            raise exceptions.NotFound()

        device.labels.update(labels["labels"])
        device.save(session)
        return device


def _device_labels_delete(context, device_type, device_id, labels):
    """Delete labels from the device labels list if it matches
    the given label in the query, otherwise do nothing."""
    session = get_session()
    with session.begin():
        devices = with_polymorphic(models.Device, '*')
        query = model_query(context, devices, session=session,
                            project_only=True)
        query = query.filter_by(type=device_type)
        query = query.filter_by(id=device_id)
        try:
            device = query.one()
        except sa_exc.NoResultFound:
            raise exceptions.NotFound()

        for label in labels["labels"]:
            device.labels.discard(label)
        device.save(session)
        return device


def _device_variables_update(context, device_type, device_id, data):
    """Update existing device variables or create when its not present."""
    session = get_session()
    with session.begin():
        _devices = with_polymorphic(models.Device, '*')
        query = model_query(context, _devices, session=session,
                            project_only=True)
        query = query.filter_by(type=device_type)
        query = query.filter_by(id=device_id)
        try:
            ref = query.with_for_update().one()
        except sa_exc.NoResultFound:
            raise exceptions.DeviceNotFound(device_type=device_type,
                                            id=device_id)

        for key in data:
            ref.variables[key] = data[key]

        return ref


def _device_variables_delete(context, device_type, device_id, data):
    """Delete the existing key (variable) from device data."""
    session = get_session()
    with session.begin():
        _devices = with_polymorphic(models.Device, '*')
        query = model_query(context, _devices, session=session,
                            project_only=True)
        query = query.filter_by(type=device_type)
        query = query.filter_by(id=device_id)

        try:
            ref = query.with_for_update().one()
        except sa_exc.NoResultFound:
            raise exceptions.DeviceNotFound(device_type=device_type,
                                            id=device_id)
        for key in data:
            try:
                del ref.variables[data[key]]
            except KeyError:
                pass

        return ref


def cells_get_all(context, filters):
    """Get all cells."""
    query = model_query(context, models.Cell, project_only=True)

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "name" in filters:
        query = query.filter_by(name=filters["name"])
    if "vars" in filters:
        query = add_var_filters_to_query(query, filters)

    try:
        return query.all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


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
        cell_ref = query.with_for_update().one()
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


def cells_variables_update(context, cell_id, data):
    """Update existing cells variables or create when
    its not present.
    """
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cell, session=session,
                            project_only=True)
        query = query.filter_by(id=cell_id)
        cell_ref = query.with_for_update().one()
        for key in data:
            cell_ref.variables[key] = data[key]
        return cell_ref


def cells_variables_delete(context, cell_id, data):
    """Delete the existing key from cells variables."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cell, session=session,
                            project_only=True)
        query = query.filter_by(id=cell_id)
        cell_ref = query.with_for_update().one()
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

    if "vars" in filters:
        query = add_var_filters_to_query(query, filters)

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
        try:
            region.update(values)
            region.save(session)
        except db_exc.DBDuplicateEntry:
            raise exceptions.DuplicateRegion()
    return region


def regions_update(context, region_id, values):
    """Update an existing region."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)
        region_ref = query.with_for_update().one()
        region_ref.update(values)
        region_ref.save(session)
        return region_ref


def regions_delete(context, region_id):
    """Delete an existing region."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)
        query.delete()
    return


def regions_variables_update(context, region_id, data):
    """
    Update existing region variables or create when its not present.
    """
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)
        region_ref = query.with_for_update().one()
        for key in data:
            region_ref.variables[key] = data[key]
        return region_ref


def regions_variables_delete(context, region_id, data):
    """Delete the existing key from region variables."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Region, session=session,
                            project_only=True)
        query = query.filter_by(id=region_id)
        region_ref = query.with_for_update().one()
        for key in data:
            try:
                del region_ref.variables[data[key]]
            except KeyError:
                # This key does not exist so just ignore
                pass
        return region_ref


def hosts_get_all(context, filters):
    """Get all hosts matching filters.

    :param filters: filters which contains different keys/values to match.
    Supported filters are region_id, name, ip_address, id, cell, device_type,
    label and vars.
    """
    host_devices = with_polymorphic(models.Device, [models.Host])
    query = model_query(context, host_devices, project_only=True)
    query = query.filter_by(type='hosts')

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
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
    if "label" in filters:
        query = query.join(models.Device.related_labels).filter(
            models.Label.label == filters["label"])
    if "vars" in filters:
        query = add_var_filters_to_query(query, filters)

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
    query = query.filter_by(type='hosts')
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
    session = get_session()
    with session.begin():
        host_devices = with_polymorphic(models.Device, '*')
        query = model_query(context, host_devices, session=session,
                            project_only=True)
        query = query.filter_by(id=host_id)
        host_ref = query.with_for_update().one()
        host_ref.update(values)
        host_ref.save(session)
        return host_ref


def hosts_delete(context, host_id):
    """Delete an existing host."""
    session = get_session()
    with session.begin():
        host_devices = with_polymorphic(models.Device, '*')
        query = model_query(context, host_devices, session=session,
                            project_only=True)
        query = query.filter_by(type='hosts')
        query = query.filter_by(id=host_id)
        query.delete()
    return


def hosts_variables_update(context, host_id, data):
    """Update existing host variables or create when its not present."""
    return _device_variables_update(context, 'hosts', host_id, data)


def hosts_variables_delete(context, host_id, data):
    """Delete the existing key from region variables."""
    return _device_variables_delete(context, 'hosts', host_id, data)


def hosts_labels_update(context, host_id, labels):
    """Update labels for host. Add the label if it is not present
    in host labels list, otherwise do nothing."""
    return _device_labels_update(context, 'hosts', host_id, labels)


def hosts_labels_delete(context, host_id, labels):
    """Delete labels from the host labels list if it matches
    the given label in the query, otherwise do nothing."""
    return _device_labels_delete(context, 'hosts', host_id, labels)


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
    if not values.get('id'):
        values['id'] = uuidutils.generate_uuid()
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


def networks_get_all(context, filters):
    """Get all networks."""
    query = model_query(context, models.Network, project_only=True)

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "network_type" in filters:
        query = query.filter_by(network_type=filters["network_type"])
    if "cell_id" in filters:
        query = query.filter_by(cell_id=filters["cell_id"])
    if "name" in filters:
        query = query.filter_by(name=filters["name"])

    result = query.all()
    return result


def networks_get_by_id(context, network_id):
    """Get a given network by its id."""
    query = model_query(context, models.Network, project_only=True)
    query = query.filter_by(id=network_id)
    try:
        result = query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()

    return result


def networks_create(context, values):
    """Create a new network."""
    session = get_session()
    network = models.Network()
    with session.begin():
        try:
            network.update(values)
            network.save(session)
        except db_exc.DBDuplicateEntry:
            raise exceptions.DuplicateNetwork()
    return network


def networks_update(context, network_id, values):
    """Update an existing network."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Network, session=session,
                            project_only=True)
        query = query.filter_by(id=network_id)
        network_ref = query.with_for_update().one()
        network_ref.update(values)
        network_ref.save(session)
        return network_ref


def networks_delete(context, network_id):
    """Delete existing network."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Network, session=session,
                            project_only=True)
        query = query.filter_by(id=network_id)
        query.delete()
    return


def networks_variables_update(context, network_id, data):
    """Update/create networks variables variables."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Network, session=session,
                            project_only=True)
        query = query.filter_by(id=network_id)

        try:
            ref = query.with_for_update().one()
        except sa_exc.NoResultFound:
            raise exceptions.NetworkNotFound(id=network_id)

        for key in data:
            ref.variables[key] = data[key]

        return ref


def networks_variables_delete(context, network_id, data):
    """Delete the existing key from networks variables."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Network, session=session,
                            project_only=True)
        query = query.filter_by(id=network_id)

        try:
            ref = query.with_for_update().one()
        except sa_exc.NoResultFound:
            raise exceptions.NetworkNotFound(id=network_id)

        for key in data:
            try:
                del ref.variables[data[key]]
            except KeyError:
                # This key does not exist so just ignore
                pass

        return ref


def netdevices_get_all(context, filters):
    """Get all network devices."""
    devices = with_polymorphic(models.Device, [models.NetDevice])
    query = model_query(context, devices, project_only=True)
    query = query.filter_by(type='net_devices')

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "vars" in filters:
        query = add_var_filters_to_query(query, filters)

    result = query.all()
    return result


def netdevices_get_by_id(context, netdevice_id):
    """Get a given network device by its id."""
    devices = with_polymorphic(models.Device, [models.NetDevice])
    query = model_query(context, devices, project_only=True)
    query = query.filter_by(type='net_devices')
    query = query.filter_by(id=netdevice_id)
    try:
        result = query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()

    return result


def netdevices_create(context, values):
    """Create a new network device."""
    session = get_session()
    device = models.NetDevice()
    with session.begin():
        device.update(values)
        device.save(session)
    return device


def netdevices_update(context, netdevice_id, values):
    """Update existing network device"""
    session = get_session()
    with session.begin():
        device = with_polymorphic(models.Device, '*')
        query = model_query(context, device, session=session,
                            project_only=True)
        query = query.filter_by(type='net_devices')
        query = query.filter_by(id=netdevice_id)
        netdevice_ref = query.with_for_update().one()
        netdevice_ref.update(values)
        netdevice_ref.save(session)
        return netdevice_ref


def netdevices_delete(context, netdevice_id):
    """Delete existing network device."""
    session = get_session()
    with session.begin():
        device = with_polymorphic(models.Device, '*')
        query = model_query(context, device, session=session,
                            project_only=True)
        query = query.filter_by(type='net_devices')
        query = query.filter_by(id=netdevice_id)
        query.delete()


def netdevices_labels_update(context, device_id, labels):
    """Update labels for a network device. Add the label if it is not present
    in host labels list, otherwise do nothing."""
    return _device_labels_update(context, 'net_devices', device_id, labels)


def netdevices_labels_delete(context, device_id, labels):
    """Delete labels from the network device labels list if it matches
    the given label in the query, otherwise do nothing."""
    return _device_labels_delete(context, 'net_devices', device_id, labels)


def netdevices_variables_update(context, device_id, data):
    """Update/create network device variables."""
    return _device_variables_update(context, 'net_devices', device_id, data)


def netdevices_variables_delete(context, device_id, data):
    """Delete the existing key from network device variables."""
    return _device_variables_delete(context, 'net_devices', device_id, data)


def net_interfaces_get_all(context, filters):
    """Get all network interfaces."""
    query = model_query(context, models.NetInterface, project_only=True)

    if "device_id" in filters:
        query = query.filter_by(device_id=filters["device_id"])
    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "ip_address" in filters:
        query = query.filter_by(ip_address=filters["ip_address"])
    if "interface_type" in filters:
        query = query.filter_by(interface_type=filters["interface_type"])

    return query.all()


def net_interfaces_get_by_id(context, interface_id):
    """Get a given network interface by its id."""
    query = model_query(context, models.NetInterface, project_only=True)
    query = query.filter_by(id=interface_id)
    try:
        result = query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()

    return result


def net_interfaces_create(context, values):
    """Create a new network interface."""
    session = get_session()
    interface = models.NetInterface()
    with session.begin():
        interface.update(values)
        interface.save(session)
    return interface


def net_interfaces_update(context, interface_id, values):
    """Update an existing network interface."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.NetInterface, session=session,
                            project_only=True)
        query = query.filter_by(id=interface_id)
        net_interface_ref = query.with_for_update().one()
        net_interface_ref.update(values)
        net_interface_ref.save(session)
        return net_interface_ref


def net_interfaces_delete(context, interface_id):
    """Delete existing network interface."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.NetInterface, session=session,
                            project_only=True)
        query = query.filter_by(id=interface_id)
        query.delete()
