"""Defines interface for DB access."""

from collections import namedtuple

from oslo_config import cfg
from oslo_db import api as db_api

db_opts = [
    cfg.StrOpt('db_backend', default='sqlalchemy',
               help='The backend to use for DB.'),
]

CONF = cfg.CONF
CONF.register_opts(db_opts)

# entrypoint namespace for db backend
BACKEND_MAPPING = {'sqlalchemy': 'craton.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=BACKEND_MAPPING,
                                lazy=True)


# Blame supports generic blame tracking for variables
# TODO(jimbaker) add additional governance support, such as
# versioning, user, notes

Blame = namedtuple('Blame', ['source', 'variable'])


def get_user_info(context, user):
    return IMPL.get_user_info(context, user)


def resource_get_by_id(context, resources, resource_id):
    """Get resource for the unique resource id."""
    return IMPL.resource_get_by_id(context, resources, resource_id)


def variables_update_by_resource_id(context, resources, resource_id, data):
    """Update/create existing resource's variables."""
    return IMPL.variables_update_by_resource_id(
        context,
        resources,
        resource_id,
        data,
    )


def variables_delete_by_resource_id(context, resources, resource_id, data):
    """Delete the existing variables, if present, from resource's data."""
    return IMPL.variables_delete_by_resource_id(
        context,
        resources,
        resource_id,
        data,
    )


# Cells

def cells_get_all(context, filters, pagination_params):
    """Get all available cells."""
    return IMPL.cells_get_all(context, filters, pagination_params)


def cells_get_by_id(context, cell_id):
    """Get cell detail for the unique cell id."""
    return IMPL.cells_get_by_id(context, cell_id)


def cells_create(context, values):
    """Create a new cell."""
    return IMPL.cells_create(context, values)


def cells_update(context, cell_id, values):
    """Update an existing cell."""
    return IMPL.cells_update(context, cell_id, values)


def cells_delete(context, cell_id):
    """Delete an existing cell."""
    return IMPL.cells_delete(context, cell_id)


def cells_variables_update(context, cell_id, data):
    """Update existing cells variables or create when
    its not present.
    """
    return IMPL.cells_variables_update(context, cell_id, data)


def cells_variables_delete(context, cell_id, data_key):
    """Delete the existing variable from cells data."""
    return IMPL.cells_variables_delete(context, cell_id, data_key)

# Regions


def regions_get_all(context, filters, pagination_params):
    """Get all available regions."""
    return IMPL.regions_get_all(context, filters, pagination_params)


def regions_get_by_name(context, name):
    """Get cell detail for the region with given name."""
    return IMPL.regions_get_by_name(context, name)


def regions_get_by_id(context, region_id):
    """Get cell detail for the region with given id."""
    return IMPL.regions_get_by_id(context, region_id)


def regions_create(context, values):
    """Create a new region."""
    return IMPL.regions_create(context, values)


def regions_update(context, region_id, values):
    """Update an existing region."""
    return IMPL.regions_update(context, region_id, values)


def regions_delete(context, region_id):
    """Delete an existing region."""
    return IMPL.regions_delete(context, region_id)


def regions_variables_update(context, region_id, data):
    """
    Update existing region variables or create when its not present.
    """
    return IMPL.regions_variables_update(context, region_id, data)


def regions_variables_delete(context, region_id, data_key):
    """Delete the existing variables from region data."""
    return IMPL.regions_variables_delete(context, region_id, data_key)

# Hosts


def hosts_get_all(context, filters, pagination_params):
    """Get all hosts."""
    return IMPL.hosts_get_all(context, filters, pagination_params)


def hosts_get_by_id(context, host_id):
    """Get details for the host with given id."""
    return IMPL.hosts_get_by_id(context, host_id)


def hosts_create(context, values):
    """Create a new host."""
    return IMPL.hosts_create(context, values)


def hosts_update(context, host_id, values):
    """Update an existing host."""
    return IMPL.hosts_update(context, host_id, values)


def hosts_delete(context, host_id):
    """Delete an existing host."""
    return IMPL.hosts_delete(context, host_id)


def hosts_labels_delete(context, host_id, labels):
    """Delete existing device label(s)."""
    return IMPL.hosts_labels_delete(context, host_id, labels)


def hosts_labels_update(context, host_id, labels):
    """Update existing device label entirely."""
    return IMPL.hosts_labels_update(context, host_id, labels)


# Projects

def projects_get_all(context, filters, pagination_params):
    """Get all the projects."""
    return IMPL.projects_get_all(context, filters, pagination_params)


def projects_get_by_name(context, project_name, filters, pagination_params):
    """Get all projects that match the given name."""
    return IMPL.projects_get_by_name(context, project_name, filters,
                                     pagination_params)


def projects_get_by_id(context, project_id):
    """Get project by its id."""
    return IMPL.projects_get_by_id(context, project_id)


def projects_create(context, values):
    """Create a new project with given values."""
    return IMPL.projects_create(context, values)


def projects_delete(context, project_id):
    """Delete an existing project given by its id."""
    return IMPL.projects_delete(context, project_id)


# Users

def users_get_all(context, filters, pagination_params):
    """Get all the users."""
    return IMPL.users_get_all(context, filters, pagination_params)


def users_get_by_name(context, user_name, filters, pagination_params):
    """Get all users that match the given username."""
    return IMPL.users_get_by_name(context, user_name, filters,
                                  pagination_params)


def users_get_by_id(context, user_id):
    """Get user by its id."""
    return IMPL.users_get_by_id(context, user_id)


def users_create(context, values):
    """Create a new user with given values."""
    return IMPL.users_create(context, values)


def users_delete(context, user_id):
    """Delete an existing user given by its id."""
    return IMPL.users_delete(context, user_id)


# Networks

def networks_get_all(context, filters, pagination_params):
    """Get all networks for the given region."""
    return IMPL.networks_get_all(context, filters, pagination_params)


def networks_get_by_id(context, network_id):
    """Get a given network by its id."""
    return IMPL.networks_get_by_id(context, network_id)


def networks_create(context, values):
    """Create a new network."""
    return IMPL.networks_create(context, values)


def networks_update(context, network_id, values):
    """Update an existing network."""
    return IMPL.networks_update(context, network_id, values)


def networks_delete(context, network_id):
    """Delete existing network."""
    return IMPL.networks_delete(context, network_id)


def networks_variables_update(context, network_id, data):
    """Update/create network variables data."""
    return IMPL.networks_variables_update(context, network_id, data)


def networks_variables_delete(context, network_id, data):
    """Delete network variables data."""
    return IMPL.networks_variables_delete(context, network_id, data)


def network_devices_get_all(context, filters, pagination_params):
    """Get all network devices."""
    return IMPL.network_devices_get_all(context, filters, pagination_params)


def network_devices_get_by_id(context, network_device_id):
    """Get a given network device by its id."""
    return IMPL.network_devices_get_by_id(context, network_device_id)


def network_devices_create(context, values):
    """Create a new network device."""
    return IMPL.network_devices_create(context, values)


def network_devices_update(context, network_device_id, values):
    """Update an existing network device"""
    return IMPL.network_devices_update(context, network_device_id, values)


def network_devices_delete(context, network_device_id):
    """Delete existing network device."""
    return IMPL.network_devices_delete(context, network_device_id)


def network_devices_labels_delete(context, network_device_id, labels):
    """Delete network device labels."""
    return IMPL.network_devices_labels_delete(context, network_device_id,
                                              labels)


def network_devices_labels_update(context, network_device_id, labels):
    """Update network device labels."""
    return IMPL.network_devices_labels_update(context, network_device_id,
                                              labels)


def network_interfaces_get_all(context, filters, pagination_params):
    """Get all network interfaces."""
    return IMPL.network_interfaces_get_all(
        context, filters, pagination_params,
    )


def network_interfaces_get_by_id(context, interface_id):
    """Get a given network interface by its id."""
    return IMPL.network_interfaces_get_by_id(context, interface_id)


def network_interfaces_create(context, values):
    """Create a new network interface."""
    return IMPL.network_interfaces_create(context, values)


def network_interfaces_update(context, interface_id, values):
    """Update an existing network interface."""
    return IMPL.network_interfaces_update(context, interface_id, values)


def network_interfaces_delete(context, interface_id):
    """Delete existing network interface."""
    return IMPL.network_interfaces_delete(context, interface_id)
