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


def get_user_info(context, user):
    return IMPL.get_user_info(context, user)


# Devices

Blame = namedtuple('Blame', ['source', 'variable'])


def device_blame_variables(device, keys=None):
    """Determines the sources of how variables have been set for a device.
    :param device: device to get blame information
    :param keys: keys to check sourcing, or all keys if None

    Returns the (source, variable) in a named tuple; note that
    variable contains certain audit/governance information
    (created_at, modified_at).

    TODO(jimbaker) further extend schema on mixed-in variable tables
    to capture additional governance, such as user who set the key;
    this will then transparently become available in the blame.
    """
    if keys is None:
        keys = device.resolved.keys()
    sources = [device] + list(device.labels) + [device.cell, device.region]
    blamed = {}
    for key in keys:
        for source in sources:
            try:
                blamed[key] = Blame(source, source._variables[key])
                break
            except KeyError:
                pass
    return blamed


# Cells

def cells_get_all(context, region):
    """Get all available cells."""
    return IMPL.cells_get_all(context, region)


def cells_get_by_name(context, region, cell):
    """Get cell detail for the cell in given region."""
    return IMPL.cells_get_by_name(context, region, cell)


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


def cells_data_update(context, cell_id, data):
    """Update existing cells variables or create when
    its not present.
    """
    return IMPL.cells_data_update(context, cell_id, data)


def cells_data_delete(context, cell_id, data_key):
    """Delete the existing key (variable) from cells data."""
    return IMPL.cells_data_delete(context, cell_id, data_key)

# Regions


def regions_get_all(context):
    """Get all available regions."""
    return IMPL.regions_get_all(context)


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


def regions_data_update(context, region_id, data):
    """
    Update existing region variables or create when its not present.
    """
    return IMPL.regions_data_update(context, region_id, data)


def regions_data_delete(context, region_id, data_key):
    """Delete the existing key (variable) from region data."""
    return IMPL.regions_data_delete(context, region_id, data_key)

# Hosts


def hosts_get_by_region_cell(context, region_id, cell_id, filters):
    """Get all hosts for region/cell."""
    return IMPL.hosts_get_by_region_cell(context, region_id, cell_id, filters)


def hosts_get_by_region(context, region_id, filters):
    """Get all hosts for this region."""
    return IMPL.hosts_get_by_region(context, region_id, filters)


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


def hosts_data_update(context, host_id, data):
    """
    Update existing host variables or create them when not present.
    """
    return IMPL.hosts_data_update(context, host_id, data)


def hosts_data_delete(context, host_id, data_key):
    """Delete the existing key (variable) from region data."""
    return IMPL.hosts_data_delete(context, host_id, data_key)


def hosts_labels_delete(context, host_id, labels):
    """Delete existing device label(s)."""
    return IMPL.hosts_labels_delete(context, host_id, labels)


def hosts_labels_update(context, host_id, labels):
    """Update existing device label entirely."""
    return IMPL.hosts_labels_update(context, host_id, labels)


# Projects

def projects_get_all(context):
    """Get all the projects."""
    return IMPL.projects_get_all(context)


def projects_get_by_name(context, project_name):
    """Get all projects that match the given name."""
    return IMPL.projects_get_by_name(context, project_name)


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

def users_get_all(context):
    """Get all the users."""
    return IMPL.users_get_all(context)


def users_get_by_name(context, user_name):
    """Get all users that match the given username."""
    return IMPL.users_get_by_name(context, user_name)


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

def networks_get_by_region(context, region_id, filters):
    """Get all networks for the given region."""
    return IMPL.networks_get_by_region(context, region_id, filters)


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


def networks_data_update(context, network_id, data):
    """Update/create network variables data."""
    return IMPL.networks_data_update(context, network_id, data)


def networks_data_delete(context, network_id, data):
    """Delete network variables data."""
    return IMPL.networks_data_delete(context, network_id, data)


def netdevices_get_by_region(context, region_id, filters):
    """Get all network devices for the given region id."""
    return IMPL.netdevices_get_by_region(context, region_id, filters)


def netdevices_get_by_id(context, netdevice_id):
    """Get a given network device by its id."""
    return IMPL.netdevices_get_by_id(context, netdevice_id)


def netdevices_create(context, values):
    """Create a new network device."""
    return IMPL.netdevices_create(context, values)


def netdevices_update(context, netdevice_id, values):
    """Update an existing network device"""
    return IMPL.netdevices_update(context, netdevice_id, values)


def netdevices_delete(context, netdevice_id):
    """Delete existing network device."""
    return IMPL.netdevices_delete(context, netdevice_id)


def netdevices_data_delete(context, netdevice_id, data):
    """Delete network device data."""
    return IMPL.netdevices_data_delete(context, netdevice_id, data)


def netdevices_data_update(context, netdevice_id, data):
    """Update network device data."""
    return IMPL.netdevices_data_update(context, netdevice_id, data)


def netdevices_labels_delete(context, netdevice_id, labels):
    """Delete network device labels."""
    return IMPL.netdevices_labels_delete(context, netdevice_id, labels)


def netdevices_labels_update(context, netdevice_id, labels):
    """Update network device labels."""
    return IMPL.netdevices_labels_update(context, netdevice_id, labels)


def net_interfaces_get_by_device(context, device_id, filters):
    """Get all network interfaces for the given device."""
    return IMPL.net_interfaces_get_by_device(context, device_id, filters)


def net_interfaces_get_by_id(context, interface_id):
    """Get a given network interface by its id."""
    return IMPL.net_interfaces_get_by_id(context, interface_id)


def net_interfaces_create(context, values):
    """Create a new network interface."""
    return IMPL.net_interfaces_create(context, values)


def net_interfaces_update(context, interface_id, values):
    """Update an existing network interface."""
    return IMPL.net_interfaces_update(context, interface_id, values)


def net_interfaces_delete(context, interface_id):
    """Delete existing network interface."""
    return IMPL.net_interfaces_delete(context, interface_id)
