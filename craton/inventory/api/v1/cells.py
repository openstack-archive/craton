from flask import request, g
from oslo_serialization import jsonutils

from craton.inventory.api.v1 import base
from craton.inventory import db as dbapi

class Cells(base.Resource):

    def get(self):
        """Get cell(s) for the project. Get cell details if
        for a particular region.
        """
        region =  g.args["region"]
        cell = g.args["name"]
        context = request.environ.get('context')

        if region != 'None' and cell != 'None':
            # Get this particular cell along with its data
            cell_obj = dbapi.cells_get_by_name(context, region, cell)
            if cell_obj:
                cell_obj.data = cell_obj.variables
                cell = jsonutils.to_primitive(cell_obj)
                return [cell], 200, None
            else:
                return [], 404, None

        if region == 'None':
            # Get all cells for all regions
            cell_obj = dbapi.cells_get_all(context, None)
            cell = jsonutils.to_primitive(cell_obj)
            return cell, 200, None

    def post(self):
        """Create a new cell."""
        context = request.environ.get('context')
        try:
            dbapi.cells_create(context, g.json)
        except Exception as err:
            LOG.error("Error during cell create: %s" % err)
            return None, 500, None

        return None, 200, None

    def put(self, id):
        """Update existing cell."""
        context = request.environ.get('context')
        try:
            dbapi.cells_update(context, cell_id, g.json)
        except Exception as err:
            LOG.error("Error during cell update: %s" % err)
            return None, 500, None

        return None, 200, None

    def delete(self, id):
        """Delete existing cell."""
        context = request.environ.get('context')
        try:
            dbapi.cells_delete(context, cell_id)
        except Exception as err:
            LOG.error("Error during cell delete: %s" % err)
            return None, 500, None

        return None, 200, None


class CellsData(base.Resource):

    def put(self, id):
        """
        Update existing cell data, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        try:
            dbapi.cells_data_update(context, cell_id, g.json)
        except Exception as err:
            LOG.error("Error during cell data update: %s" % err)
            return None, 500, None

        return None, 200, None

    def delete(self, id):
        """Delete cell data."""
        context = request.environ.get('context')
        try:
            dbapi.cells_data_delete(context, cell_id, g.json)
        except Exception as err:
            LOG.error("Error during cell delete: %s" % err)
            return None, 500, None

        return None, 200, None
