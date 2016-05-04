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

def cells_get_all(context):
    """Get all available cells."""
    return IMPL.cells_get_all(context)


def cells_get_by_filters(filters):
    """Get cells that match given filters."""
    return IMPL.cells_get_by_filters(filters)
