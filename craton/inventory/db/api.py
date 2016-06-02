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
BACKEND_MAPPING = {'sqlalchemy': 'craton.inventory.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=BACKEND_MAPPING,
                                lazy=True)


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
    sources = [device] + list(device.labels) + [device.region, device.cell]
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


def cells_get_by_id(context, region_id, cell_id):
    """Get cell detail for the cell id in given region."""
    return IMPL.cells_get_by_id(context, region_id, cell_id)


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
