"""SQLAlchemy backend implementation."""

import enum
import functools
from operator import attrgetter
import sys
import uuid

import jsonpath_rw as jspath

from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_log import log

from sqlalchemy import and_, sql
from sqlalchemy import func as sa_func
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

MYSQL_INVALID_JSONPATH_EXPRESSION = 3143
MYSQL_INVALID_JSON_TEXT = 3141

JSON_EXCEPTIONS = {
    MYSQL_INVALID_JSONPATH_EXPRESSION: exceptions.InvalidJSONPath(),
    MYSQL_INVALID_JSON_TEXT: exceptions.InvalidJSONValue(),
}


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
        context = args[0]
        if is_project_admin_context(context):
            return f(*args, **kwargs)
        elif is_project_admin_context(args[0]):
            return f(*args, **kwargs)
        else:
            raise exceptions.AdminRequired()
    return wrapper


class CRUD(enum.Enum):
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'


def permissions_for(action):
    # NOTE(thomasem): Temporary shim applying existing project admin / root
    # project checks to generic resource methods, since we don't have RBAC
    # fully baked yet. This needs to be removed once we have solved this via
    # craton-rbac-support blueprint. This affords us being able to use
    # generic resource methods support for resources like Projects, where one
    # must be Project admin to interact.
    def get_permissions_for(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # NOTE(thomasem): Standard order of arguments for generic resources
            # methods is (context, resources, ...), so args[0] is always
            # context and args[1] is always resources.
            context = args[0]
            resources = args[1]
            permissions = {
                CRUD.CREATE: {
                    'projects': is_project_admin_context(context),
                },
                CRUD.READ: {
                    'projects': is_project_admin_context(context),
                },
                CRUD.UPDATE: {
                    'projects': is_project_admin_context(context),
                },
                CRUD.DELETE: {
                    'projects': is_project_admin_context(context),
                }
            }
            # NOTE(thomasem): Default to True unless otherwise specified in
            # permissions dict.
            if permissions[action].get(resources, True):
                return fn(*args, **kwargs)
            else:
                raise exceptions.AdminRequired()
        return wrapper
    return get_permissions_for


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


def _find_first_key_fragment(root):
    """Finds element where first key Field exists."""
    desired = jspath.Fields
    if isinstance(root, desired):
        return root
    while not isinstance(root.left, desired):
        root = root.left
    return root


def _split_key_path_prefix(root):
    """Extract first key and initial path from parsed JSON Path.

    This is necessitated by us not actually including the top-most Key
    component in the JSON column (Variables.value) in the database, so we only
    need a parser to extract the first Key from the expression. The rest can be
    handled in the database.

    This essentially takes a parsed JSON Path, finds the first field and
    optional Slice or Index.  It then uses the value of the first field's value
    (fields[0]) as the key and, if a Slice of Index exist on the right
    side of the expression, it builds an Array specifier as the initial part of
    the path and then returns them.
    """
    # NOTE(thomasem): Because of how keys work and our data model, the first
    # element should not be anything other than a Fields or a Child fragment.
    if not isinstance(root, (jspath.Fields, jspath.Child)):
        raise exceptions.InvalidJSONPath()

    path = ''
    fragment = _find_first_key_fragment(root)
    right = getattr(fragment, 'right', None)
    left = getattr(fragment, 'left', None) or fragment

    if isinstance(right, jspath.Slice) and any([right.start, right.end]):
        # NOTE(thomasem): MySQL 5.7 does not support arbitrary slices, only
        # '[*]'.
        raise exceptions.InvalidJSONPath()
    elif isinstance(right, jspath.Slice):
        path = '[*]'
    elif isinstance(right, jspath.Index):
        path = '[{}]'.format(right.index)

    key = left.fields[0]
    return key, path


def _parse_path_expr(path_expression):
    """Split into the first key and the path used for querying MySQL."""
    try:
        parsed = jspath.parse(path_expression)
    except Exception:
        # NOTE(thomasem): Unfortunately, this library raises an Exception
        # instead of something more specific.
        raise exceptions.InvalidJSONPath() from e

    # NOTE(thomasem): Get the first key from the parsed JSON Path expression
    # and initial path for the Variables.value JSON column, if there is any.
    # There would only be an initial path if there's an Array specifier
    # immediately adjacent to the first key, for example: 'foo[5]' or 'foo[*]'.
    key, path = _split_key_path_prefix(parsed)

    # NOTE(thomasem): Remove the key we found from the original expression
    # since that's not included in the Variables.value JSON column.
    key_removed = path_expression[len(key):]

    # NOTE(thomasem): Because the first key could have been wrapped in quotes
    # to denote it as a JSON string for handling special characters in the
    # key, we will want to find the first delimiter ('.') if one exists to
    # know where to slice off the remainder of the path and combine prefix
    # and suffix.
    path_suffix_start = key_removed.find('.')
    if path_suffix_start > -1:
        path = '{}{}'.format(path, key_removed[path_suffix_start:])
    return key, '${}'.format(path)


def _json_path_clause(kv_pair):
    path_expr, value = kv_pair
    key, path = _parse_path_expr(path_expr)

    json_match = sa_func.json_contains(
        sa_func.json_extract(models.Variable.value, path), value)

    # NOTE(thomasem): Order is important here. MySQL will short-circuit and
    # not properly validate the JSON Path expression when the key doesn't exist
    # if the key match is first int he and_(...) expression. So, let's put
    # the json_match first.
    return and_(json_match, models.Variable.key == key)


def _get_variables(query):
    try:
        return set(query)
    except db_exc.DBError as e:
        orig = getattr(e.inner_exception, 'orig', None)
        code = orig.args[0]
        if orig and code in JSON_EXCEPTIONS:
            raise JSON_EXCEPTIONS[code] from e
        raise


def _matching_resources(query, resource_cls, get_descendants, kv):

    # NOTE(jimbaker) Build a query that determine all resources that
    # match this key/value, taking in account variable
    # resolution. Note that this value is generalized to be a JSON
    # path; and the resolution is inverted by finding any possible
    # descendants.

    kv_pairs = list(kv.items())
    matches = {}
    for kv_pair in kv_pairs:
        match = matches[kv_pair] = set()
        kv_clause = _json_path_clause(kv_pair)
        matching_variables = _get_variables(
            query.session.query(models.Variable).filter(kv_clause))

        for variable in matching_variables:
            if isinstance(variable.parent, resource_cls):
                match.add(variable.parent)

            # NOTE(jimbaker) now check for descendent overrides; in
            # particular, it's possible that a chain of overrides
            # could occur such that the original top value was
            # restored.
            #
            # Because all of the matching variables were returned by
            # the query; and SQLAlchemy guarantees that within the
            # scope of a transaction ("unit of work") that a given
            # object will have the same identity, we can check with
            # respect to matching_variables. Do note that arbitrary
            # additional object graph queries may be done to check the
            # resolution ordering.

            for descendant in get_descendants(variable.parent):
                for level in descendant.resolution_order:
                    desc_variable = level._variables.get(variable.key)
                    if desc_variable is not None:
                        if desc_variable in matching_variables:
                            match.add(descendant)
                        break

    # NOTE(jimbaker) For now, we simply match for the conjunction
    # ("and") of all the supplied kv pairs we are matching
    # against. Generalize in the future as desired with other boolean
    # logic.
    _, first_match = matches.popitem()
    if matches:
        resources = first_match.intersection(*matches.values())
    else:
        resources = first_match
    return resources


def _get_devices(parent):
    if isinstance(parent, models.Device):
        return parent.descendants
    else:
        return parent.devices


_resource_mapping = {
    models.Project: ([], None),
    models.Cloud: ([models.Project], attrgetter('clouds')),
    models.Region: ([models.Project, models.Cloud], attrgetter('regions')),
    models.Cell: (
        [models.Project, models.Cloud, models.Region],
        attrgetter('cells')),
    models.Network: (
        [models.Project, models.Cloud, models.Region, models.Cell],
        attrgetter('networks')),
    models.Device: (
        [models.Project, models.Cloud, models.Region, models.Cell,
         models.Device],
        _get_devices),
}


def matching_resources(query, resource_cls, kv, resolved):
    def get_desc(parent):
        parent_classes, getter = _resource_mapping[resource_cls]
        # NOTE(thomasem): If we're not resolving, there are no descendants
        # to process, so return an empty list.
        if resolved and any(isinstance(parent, cls) for cls in parent_classes):
            return getter(parent)
        else:
            return []

    return _matching_resources(query, resource_cls, get_desc, kv)


def _add_var_filters_to_query(query, model, var_filters, resolved=True):
    # vars filters are of form ?vars=a:b[,c:d,...] - the filters in
    # this case are intersecting ("and" queries)
    kv = dict(pairing.split(':', 1) for pairing in var_filters)
    resource_ids = set(
        resource.id
        for resource in matching_resources(query, model, kv, resolved)
    )
    if not resource_ids:
        # short circuit; this also avoids SQLAlchemy reporting that it is
        # working with an empty "in" clause
        return query.filter(sql.false())
    return query.filter(model.id.in_(resource_ids))


def add_var_filters_to_query(query, model, filters):
    var_filters = filters['vars'].split(',')
    resolved = bool(filters.get('resolved-values'))
    return _add_var_filters_to_query(query, model, var_filters,
                                     resolved=resolved)


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


def _get_resource_model(resource):
    resource_models = {
        "cells": models.Cell,
        "devices": with_polymorphic(models.Device, "*"),
        "hosts": with_polymorphic(models.Device, models.Host),
        "network-devices": with_polymorphic(
            models.Device, models.NetworkDevice
        ),
        "networks": models.Network,
        "regions": models.Region,
        "clouds": models.Cloud,
        "projects": models.Project,
    }
    return resource_models[resource]


@permissions_for(CRUD.READ)
def resource_get_by_id(
        context, resources, resource_id, session=None, for_update=False
        ):
    """Get resource for the unique resource id."""
    model = _get_resource_model(resources)

    query = model_query(context, model, project_only=True, session=session)

    if resources in ("hosts", "network-devices"):
        query = query.filter_by(type=resources.replace("-", "_"))

    query = query.filter_by(id=resource_id)

    if for_update:
        query = query.with_for_update()

    try:
        resource = query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    else:
        return resource


@permissions_for(CRUD.UPDATE)
def variables_update_by_resource_id(context, resources, resource_id, data):
    """Update/create existing resource's variables."""
    session = get_session()
    with session.begin():
        resource = resource_get_by_id(
            context, resources, resource_id, session, for_update=True
        )

        resource.variables.update(data)
        return resource


@permissions_for(CRUD.DELETE)
def variables_delete_by_resource_id(context, resources, resource_id, data):
    """Delete the existing variables, if present, from resource's data."""
    session = get_session()
    with session.begin():
        resource = resource_get_by_id(
            context, resources, resource_id, session, for_update=True
        )

        for key in data:
            try:
                del resource.variables[key]
            except KeyError:
                pass
        return resource


def devices_get_all(context, filters, pagination_params):
    """Get all available devices."""
    session = get_session()
    devices = with_polymorphic(models.Device, "*")
    query = model_query(context, devices, project_only=True, session=session)

    if "parent_id" in filters and filters.get("descendants"):
        parent = query.filter_by(id=filters["parent_id"]).one()
        query = query.filter(
            models.Device.id.in_(device.id for device in parent.descendants)
        )
    elif "parent_id" in filters:
        query = query.filter_by(parent_id=filters["parent_id"])

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "cloud_id" in filters:
        query = query.filter_by(cloud_id=filters["cloud_id"])
    if "cell_id" in filters:
        query = query.filter_by(cell_id=filters["cell_id"])
    if "active" in filters:
        query = query.filter_by(active=filters["active"])

    return _paginate(context, query, models.Device, session, filters,
                     pagination_params)


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


def cells_get_all(context, filters, pagination_params):
    """Get all cells."""
    session = get_session()
    query = model_query(context, models.Cell, project_only=True,
                        session=session)

    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "cloud_id" in filters:
        query = query.filter_by(cloud_id=filters["cloud_id"])
    if "name" in filters:
        query = query.filter_by(name=filters["name"])
    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Cell, filters)

    return _paginate(context, query, models.Cell, session, filters,
                     pagination_params)


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
        try:
            cell.update(values)
            cell.save(session)
        except db_exc.DBDuplicateEntry:
            raise exceptions.DuplicateCell()
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


def regions_get_all(context, filters, pagination_params):
    """Get all available regions."""
    session = get_session()
    query = model_query(context, models.Region, project_only=True,
                        session=session)

    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Region, filters)
    if "cloud_id" in filters:
        query = query.filter_by(cloud_id=filters["cloud_id"])

    return _paginate(context, query, models.Region, session, filters,
                     pagination_params)


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


def clouds_get_all(context, filters, pagination_params):
    """Get all available clouds."""
    session = get_session()
    query = model_query(context, models.Cloud, project_only=True,
                        session=session)

    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Cloud, filters)

    return _paginate(context, query, models.Cloud, session, filters,
                     pagination_params)


def clouds_get_by_name(context, name):
    """Get cell detail for the cloud with given name."""
    query = model_query(context, models.Cloud, project_only=True)
    query = query.filter_by(name=name)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


def clouds_get_by_id(context, cloud_id):
    """Get cell detail for the cloud with given id."""
    query = model_query(context, models.Cloud, project_only=True)
    query = query.filter_by(id=cloud_id)
    try:
        return query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()


def clouds_create(context, values):
    """Create a new cloud."""
    session = get_session()
    cloud = models.Cloud()
    with session.begin():
        try:
            cloud.update(values)
            cloud.save(session)
        except db_exc.DBDuplicateEntry:
            raise exceptions.DuplicateCloud()
    return cloud


def clouds_update(context, cloud_id, values):
    """Update an existing cloud."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cloud, session=session,
                            project_only=True)
        query = query.filter_by(id=cloud_id)
        cloud_ref = query.with_for_update().one()
        cloud_ref.update(values)
        cloud_ref.save(session)
        return cloud_ref


def clouds_delete(context, cloud_id):
    """Delete an existing cloud."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.Cloud, session=session,
                            project_only=True)
        query = query.filter_by(id=cloud_id)
        query.delete()
    return


def hosts_get_all(context, filters, pagination_params):
    """Get all hosts matching filters.

    :param filters: filters which contains different keys/values to match.
    Supported filters are region_id, name, ip_address, id, cell, device_type,
    label and vars.
    """
    session = get_session()
    host_devices = with_polymorphic(models.Device, [models.Host])
    query = model_query(context, host_devices, project_only=True,
                        session=session)
    query = query.filter_by(type='hosts')

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "cloud_id" in filters:
        query = query.filter_by(cloud_id=filters["cloud_id"])
    if "name" in filters:
        query = query.filter_by(name=filters["name"])
    if "ip_address" in filters:
        query = query.filter_by(ip_address=filters["ip_address"])
    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "cell_id" in filters:
        query = query.filter_by(cell_id=filters["cell_id"])
    if "device_type" in filters:
        query = query.filter_by(device_type=filters["device_type"])
    if "label" in filters:
        query = query.filter(models.Device.related_labels.any(
            models.Label.label == filters["label"]))
    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Device, filters)

    return _paginate(context, query, models.Host, session, filters,
                     pagination_params)


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
        try:
            host.update(values)
            host.save(session)
        except db_exc.DBDuplicateEntry:
            raise exceptions.DuplicateDevice()
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
        try:
            host_ref.update(values)
        except exceptions.ParentIDError as e:
            raise exceptions.BadRequest(message=str(e))
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


def hosts_labels_update(context, host_id, labels):
    """Update labels for host. Add the label if it is not present
    in host labels list, otherwise do nothing."""
    return _device_labels_update(context, 'hosts', host_id, labels)


def hosts_labels_delete(context, host_id, labels):
    """Delete labels from the host labels list if it matches
    the given label in the query, otherwise do nothing."""
    return _device_labels_delete(context, 'hosts', host_id, labels)


@require_admin_context
def projects_get_all(context, filters, pagination_params):
    """Get all the projects."""
    session = get_session()
    query = model_query(context, models.Project, session=session)
    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Project, filters)
    return _paginate(context, query, models.Project, session, filters,
                     pagination_params)


@require_admin_context
def projects_get_by_name(context, project_name, filters, pagination_params):
    """Get all projects that match the given name."""
    query = model_query(context, models.Project)
    query = query.filter(models.Project.name.like(project_name))
    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Project, filters)
    try:
        return _paginate(context, query, models.Project, session, filters,
                         pagination_params)
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except Exception as err:
        raise exceptions.UnknownException(message=err)


@require_project_admin_context
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
        values['id'] = uuid.uuid4()
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
def users_get_all(context, filters, pagination_params):
    """Get all the users."""
    session = get_session()
    if is_admin_context(context):
        LOG.info("Getting all users as root user")
        query = model_query(context, models.User, session=session)
    else:
        LOG.info("Getting all users as project admin user")
        query = model_query(context, models.User, project_only=True,
                            session=session)
        query = query.filter_by(project_id=context.tenant)

    return _paginate(context, query, models.User, session, filters,
                     pagination_params)


@require_project_admin_context
def users_get_by_name(context, user_name, filters, pagination_params):
    """Get all users that match the given username."""
    session = get_session()
    if is_admin_context(context):
        query = model_query(context, models.User, session=session)
    else:
        query = model_query(context, models.User, project_only=True,
                            session=session)

    query = query.filter_by(username=user_name)
    return _paginate(context, query, models.User, session, filters,
                     pagination_params)


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


def networks_get_all(context, filters, pagination_params):
    """Get all networks."""
    session = get_session()
    query = model_query(context, models.Network, project_only=True,
                        session=session)

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
    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Network, filters)

    return _paginate(context, query, models.Network, session, filters,
                     pagination_params)


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


def network_devices_get_all(context, filters, pagination_params):
    """Get all network devices."""
    session = get_session()
    devices = with_polymorphic(models.Device, [models.NetworkDevice])
    query = model_query(context, devices, project_only=True, session=session)
    query = query.filter_by(type='network_devices')

    if "region_id" in filters:
        query = query.filter_by(region_id=filters["region_id"])
    if "cloud_id" in filters:
        query = query.filter_by(cloud_id=filters["cloud_id"])
    if "name" in filters:
        query = query.filter_by(name=filters["name"])
    if "ip_address" in filters:
        query = query.filter_by(ip_address=filters["ip_address"])
    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "cell_id" in filters:
        query = query.filter_by(cell_id=filters["cell_id"])
    if "device_type" in filters:
        query = query.filter_by(device_type=filters["device_type"])
    if "vars" in filters:
        query = add_var_filters_to_query(query, models.Device, filters)

    return _paginate(context, query, models.Device, session, filters,
                     pagination_params)


def network_devices_get_by_id(context, network_device_id):
    """Get a given network device by its id."""
    devices = with_polymorphic(models.Device, [models.NetworkDevice])
    query = model_query(context, devices, project_only=True)
    query = query.filter_by(type='network_devices')
    query = query.filter_by(id=network_device_id)
    try:
        result = query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()

    return result


def network_devices_create(context, values):
    """Create a new network device."""
    session = get_session()
    device = models.NetworkDevice()
    with session.begin():
        device.update(values)
        device.save(session)
    return device


def network_devices_update(context, network_device_id, values):
    """Update existing network device"""
    session = get_session()
    with session.begin():
        device = with_polymorphic(models.Device, '*')
        query = model_query(context, device, session=session,
                            project_only=True)
        query = query.filter_by(type='network_devices')
        query = query.filter_by(id=network_device_id)
        network_device_ref = query.with_for_update().one()
        try:
            network_device_ref.update(values)
        except exceptions.ParentIDError as e:
            raise exceptions.BadRequest(message=str(e))
        network_device_ref.save(session)
        return network_device_ref


def network_devices_delete(context, network_device_id):
    """Delete existing network device."""
    session = get_session()
    with session.begin():
        device = with_polymorphic(models.Device, '*')
        query = model_query(context, device, session=session,
                            project_only=True)
        query = query.filter_by(type='network_devices')
        query = query.filter_by(id=network_device_id)
        query.delete()


def network_devices_labels_update(context, device_id, labels):
    """Update labels for a network device. Add the label if it is not present
    in host labels list, otherwise do nothing."""
    return _device_labels_update(context, 'network_devices', device_id, labels)


def network_devices_labels_delete(context, device_id, labels):
    """Delete labels from the network device labels list if it matches
    the given label in the query, otherwise do nothing."""
    return _device_labels_delete(context, 'network_devices', device_id, labels)


def network_interfaces_get_all(context, filters, pagination_params):
    """Get all network interfaces."""
    session = get_session()
    query = model_query(context, models.NetworkInterface, project_only=True,
                        session=session)

    if "device_id" in filters:
        query = query.filter_by(device_id=filters["device_id"])
    if "id" in filters:
        query = query.filter_by(id=filters["id"])
    if "ip_address" in filters:
        query = query.filter_by(ip_address=filters["ip_address"])
    if "interface_type" in filters:
        query = query.filter_by(interface_type=filters["interface_type"])

    return _paginate(context, query, models.NetworkInterface, session,
                     filters, pagination_params)


def network_interfaces_get_by_id(context, interface_id):
    """Get a given network interface by its id."""
    query = model_query(context, models.NetworkInterface, project_only=True)
    query = query.filter_by(id=interface_id)
    try:
        result = query.one()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()

    return result


def network_interfaces_create(context, values):
    """Create a new network interface."""
    session = get_session()
    interface = models.NetworkInterface()
    with session.begin():
        interface.update(values)
        interface.save(session)
    return interface


def network_interfaces_update(context, interface_id, values):
    """Update an existing network interface."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.NetworkInterface, session=session,
                            project_only=True)
        query = query.filter_by(id=interface_id)
        network_interface_ref = query.with_for_update().one()
        network_interface_ref.update(values)
        network_interface_ref.save(session)
        return network_interface_ref


def network_interfaces_delete(context, interface_id):
    """Delete existing network interface."""
    session = get_session()
    with session.begin():
        query = model_query(context, models.NetworkInterface, session=session,
                            project_only=True)
        query = query.filter_by(id=interface_id)
        query.delete()


def _marker_from(context, session, model, marker, project_only):
    if marker is None:
        return None

    query = model_query(context, model, session=session,
                        project_only=project_only)
    return query.filter_by(id=marker).one()


def _get_previous(query, model, current_marker, page_size, filters):
    # NOTE(sigmavirus24): To get the previous items based on the existing
    # filters, we need only reverse the direction that the user requested.
    original_sort_dir = filters['sort_dir']
    sort_dir = 'desc'
    if original_sort_dir == 'desc':
        sort_dir = 'asc'

    results = db_utils.paginate_query(
        query, model,
        limit=page_size,
        sort_keys=filters['sort_keys'],
        sort_dir=sort_dir,
        marker=current_marker,
    ).all()

    if not results:
        return None

    return results[-1].id


def _link_params_for(query, model, filters, pagination_params,
                     current_marker, current_results):
    links = {}
    # We can discern our base parameters for our links
    base_parameters = {}
    for (key, value) in filters.items():
        # NOTE(thomasem): Sometimes the filters that are passed in will include
        # a None value from the schema. This causes it to not get included
        # in the link, since a None value indicates you did not include a value
        # for that parameter in the original call.
        if value is None:
            continue
        # This takes care of things like sort_keys which may have multiple
        # values
        if isinstance(value, list):
            value = ','.join(value)
        base_parameters[key] = value
    base_parameters['limit'] = pagination_params['limit']
    generate_links = ('first', 'self')

    if current_results:
        next_marker = current_results[-1]
        # If there are results to return, there may be a next link to follow
        generate_links += ('next',)

    # We start our links dictionary with some basics
    for relation in generate_links:
        params = base_parameters.copy()
        if relation == 'self':
            if pagination_params['marker'] is not None:
                params['marker'] = pagination_params['marker']
        elif relation == 'next':
            params['marker'] = next_marker.id
        links[relation] = params

    params = base_parameters.copy()
    previous_marker = None
    if current_marker is not None:
        previous_marker = _get_previous(
            query, model, current_marker, pagination_params['limit'], filters,
        )
    if previous_marker is not None:
        params['marker'] = previous_marker
    links['prev'] = params
    return links


def _paginate(context, query, model, session, filters, pagination_params,
              project_only=False):
    # NOTE(sigmavirus24) Retrieve the instance of the model represented by the
    # marker.
    try:
        marker = _marker_from(context, session, model,
                              pagination_params['marker'],
                              project_only)
    except sa_exc.NoResultFound:
        raise exceptions.BadRequest(
            message='Marker "{}" does not exist'.format(
                pagination_params['marker']
            )
        )
    except Exception as err:
        raise exceptions.UnknownException(message=err)

    filters.setdefault('sort_keys', ['created_at', 'id'])
    filters.setdefault('sort_dir', 'asc')
    # Retrieve the results based on the marker and the limit
    try:
        results = db_utils.paginate_query(
            query, model,
            limit=pagination_params['limit'],
            sort_keys=filters['sort_keys'],
            sort_dir=filters['sort_dir'],
            marker=marker,
        ).all()
    except sa_exc.NoResultFound:
        raise exceptions.NotFound()
    except db_exc.InvalidSortKey as invalid_key:
        raise exceptions.BadRequest(
            message='"{}" is an invalid sort key'.format(invalid_key.key)
        )
    except Exception as err:
        raise exceptions.UnknownException(message=err)

    try:
        links = _link_params_for(
            query, model, filters, pagination_params, marker, results,
        )
    except Exception as err:
        raise exceptions.UnknownException(message=err)

    return results, links
