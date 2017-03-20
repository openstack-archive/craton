from oslo_serialization import jsonutils
from oslo_log import log


from craton.api.v1 import base
from craton.api.v1.resources import utils
from craton import db as dbapi


# NOTE(thomasem): LOG must exist for craton.api.v1.base module to introspect
# and execute this modules LOG.
LOG = log.getLogger(__name__)


class Variables(base.Resource):

    def get(self, context, resources, id, request_args=None):
        """Get variables for given resource."""
        obj = dbapi.resource_get_by_id(context, resources, id)
        obj = utils.format_variables(request_args, obj)
        resp = {"variables": jsonutils.to_primitive(obj.vars)}
        return resp, 200, None

    def put(self, context, resources, id, request_data):
        """
        Update existing resource variables, or create if it does
        not exist.
        """
        obj = dbapi.variables_update_by_resource_id(
            context, resources, id, request_data
        )
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    def delete(self, context, resources, id, request_data):
        """Delete resource variables."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        dbapi.variables_delete_by_resource_id(
            context, resources, id, request_data
        )
        return None, 204, None
