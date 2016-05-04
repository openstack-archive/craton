"""SQLAlchemy backend implementation."""
import sys

from oslo_config import cfg
from oslo_db import exception as db_exception
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_log import log

from craton.inventory.db.sqlalchemy import models


CONF = cfg.CONF

LOG = log.getLogger(__name__)


_FACADE = None

_DEFAULT_SQL_CONNECTION = 'sqlite:////Users/sulochan.acharya/test_craton/craton/test.db'
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


def require_admin_context(f):
    """Decorator that ensures admin request context."""

    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]):
            raise exception.AdminRequired()
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
        kwargs['project_id'] = context.project_id

    return db_utils.model_query(
        model=model, session=session, args=args, **kwargs)


###################
# TODO(sulo): add filter on project_id and deleted fields

def cells_get_all(context):
    """Get all cells."""
    result = model_query(context, models.Cell).\
             all()
    return result


def cells_get_by_filters(context, filters):
    """Get all cells that match the given filters."""
    query = model_query(context, models.Cell)
    for k,v in filters.iteritems():
        query = query.filter_by(k=v)
    
    result = query.all()
    return result
