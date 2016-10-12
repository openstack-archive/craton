from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Cells(base.Resource):

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        filters=['id', 'name'])
    def get(self, context, region_id, filters):
        """Get cells for the region, with optional filtering."""
        if 'name' in filters:
            cell_obj = dbapi.cells_get_by_name(
                context, region_id, filters['name'])
            cell_obj.data = cell_obj.variables
            cells_obj = [cell_obj]
        elif 'id' in filters:
            cell_obj = dbapi.cells_get_by_id(context, filters['id'])
            cell_obj.data = cell_obj.variables
            cells_obj = [cell_obj]
        else:
            cells_obj = dbapi.cells_get_all(context, region_id)
        return jsonutils.to_primitive(cells_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new cell."""
        context = request.environ.get('context')
        cell_obj = dbapi.cells_create(context, g.json)
        return jsonutils.to_primitive(cell_obj), 200, None


class CellById(base.Resource):

    @base.http_codes
    def get(self, id):
        context = request.environ.get('context')
        cell_obj = dbapi.cells_get_by_id(context, id)
        cell_obj.data = cell_obj.variables
        cell = jsonutils.to_primitive(cell_obj)
        return cell, 200, None

    def put(self, id):
        """Update existing cell."""
        return None, 401, None

    @base.http_codes
    def delete(self, id):
        """Delete existing cell."""
        context = request.environ.get('context')
        dbapi.cells_delete(context, id)
        return None, 204, None


class CellsData(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get data for given cell."""
        context = request.environ.get('context')
        obj = dbapi.cells_get_by_id(context, id)
        resp = {"data": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, id):
        """
        Update existing cell data, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        obj = dbapi.cells_data_update(context, id, request.json)
        resp = {"data": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete cell data."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        context = request.environ.get('context')
        dbapi.cells_data_delete(context, id, request.json)
        return None, 204, None
