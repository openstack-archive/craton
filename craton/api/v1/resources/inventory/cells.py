from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Cells(base.Resource):

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all cells, with optional filtering."""
        cells_obj, link_paramss = dbapi.cells_get_all(
            context, request_args, pagination_params,
        )
        links = base.links_from(link_params)
        response_body = {'cells': cells_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new cell."""
        json = util.copy_project_id_into_json(context, request_data)
        cell_obj = dbapi.cells_create(context, json)
        cell = jsonutils.to_primitive(cell_obj)
        if 'variables' in json:
            cell["variables"] = jsonutils.to_primitive(cell_obj.variables)
        else:
            cell["variables"] = {}
        return cell, 200, None


class CellById(base.Resource):

    @base.http_codes
    def get(self, context, id):
        cell_obj = dbapi.cells_get_by_id(context, id)
        cell = jsonutils.to_primitive(cell_obj, convert_instances=True)
        cell['variables'] = jsonutils.to_primitive(cell_obj.variables)
        return cell, 200, None

    def put(self, context, id, request_data):
        """Update existing cell."""
        cell_obj = dbapi.cells_update(context, id, request_data)
        return jsonutils.to_primitive(cell_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing cell."""
        dbapi.cells_delete(context, id)
        return None, 204, None


class CellsVariables(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get variables for given cell."""
        obj = dbapi.cells_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, context, id, request_data):
        """
        Update existing cell variables, or create if it does
        not exist.
        """
        obj = dbapi.cells_variables_update(context, id, request_data)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, context, id, request_data):
        """Delete cell variables."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        dbapi.cells_variables_delete(context, id, request_data)
        return None, 204, None
