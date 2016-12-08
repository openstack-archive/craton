from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Cells(base.Resource):

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        reserved_keys=['id', 'name', 'region_id', 'vars'])
    def get(self, context, region_id, filters):
        """Get cells for the region, with optional filtering."""
        if 'name' in filters:
            cell_obj = dbapi.cells_get_by_name(
                context, region_id, filters['name'])
            cells_obj = [cell_obj]
        elif 'id' in filters:
            cell_obj = dbapi.cells_get_by_id(context, filters['id'])
            cells_obj = [cell_obj]
        else:
            cells_obj = dbapi.cells_get_all(context, region_id, filters)
        return jsonutils.to_primitive(cells_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new cell."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        cell_obj = dbapi.cells_create(context, json)
        cell = jsonutils.to_primitive(cell_obj)
        if 'variables' in json:
            cell["variables"] = jsonutils.to_primitive(cell_obj.variables)
        else:
            cell["variables"] = {}
        return cell, 200, None


class CellById(base.Resource):

    @base.http_codes
    def get(self, id):
        context = request.environ.get('context')
        cell_obj = dbapi.cells_get_by_id(context, id)
        cell = jsonutils.to_primitive(cell_obj, convert_instances=True)
        cell['variables'] = jsonutils.to_primitive(cell_obj.variables)
        return cell, 200, None

    def put(self, id):
        """Update existing cell."""
        context = request.environ.get('context')
        cell_obj = dbapi.cells_update(context, id, request.json)
        return jsonutils.to_primitive(cell_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing cell."""
        context = request.environ.get('context')
        dbapi.cells_delete(context, id)
        return None, 204, None


class CellsVariables(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get variables for given cell."""
        context = request.environ.get('context')
        obj = dbapi.cells_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, id):
        """
        Update existing cell variables, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        obj = dbapi.cells_variables_update(context, id, request.json)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete cell variables."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        context = request.environ.get('context')
        dbapi.cells_variables_delete(context, id, request.json)
        return None, 204, None
