"""Defines interface for DB access."""

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

# Cells

def cells_get_all(context, region):
    """Get all available cells."""
    return IMPL.cells_get_all(context, region)


def cells_get_by_name(context, region, cell):
    """Get cell detail for the cell in given region."""
    return IMPL.cells_get_by_name(context, region, cell)


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
