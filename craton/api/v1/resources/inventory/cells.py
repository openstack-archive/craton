from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Cells(base.Resource):

    def get(self):
        """Get cell(s) for the project. Get cell details if
        for a particular region.
        """
        region = g.args["region"]
        cell_name = g.args["name"]
        cell_id = g.args["id"]
        context = request.environ.get('context')

        if not region:
            msg = "`region` is required to get cells"
            return self.error_response(400, msg)

        if region and cell_name:
            # Get this particular cell along with its data
            try:
                cell_obj = dbapi.cells_get_by_name(context, region, cell_name)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')
            except Exception as err:
                LOG.error("Error during cells get: %s" % err)
                return self.error_response(500, 'Unknown Error')

            cell_obj.data = cell_obj.variables
            cell = jsonutils.to_primitive(cell_obj)
            return [cell], 200, None

        if region and cell_id:
            # Get this particular cell along with its data
            try:
                cell_obj = dbapi.cells_get_by_id(context, cell_id)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')
            except Exception as err:
                LOG.error("Error during cells get: %s" % err)
                return self.error_response(500, 'Unknown Error')

            cell_obj.data = cell_obj.variables
            cell = jsonutils.to_primitive(cell_obj)
            return [cell], 200, None

        # No cell id or name so get all cells for this region only
        try:
            cells_obj = dbapi.cells_get_all(context, region)
            cells = jsonutils.to_primitive(cells_obj)
            return cells, 200, None
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')

    def post(self):
        """Create a new cell."""
        context = request.environ.get('context')
        try:
            cell_obj = dbapi.cells_create(context, g.json)
        except Exception as err:
            LOG.error("Error during cell create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        cell = jsonutils.to_primitive(cell_obj)
        return cell, 200, None


class CellById(base.Resource):

    def get(self, id):
        context = request.environ.get('context')
        try:
            cell_obj = dbapi.cells_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during Cell get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        cell_obj.data = cell_obj.variables
        cell = jsonutils.to_primitive(cell_obj)
        return cell, 200, None

    def put(self, id):
        """Update existing cell."""
        return None, 401, None

    def delete(self, id):
        """Delete existing cell."""
        context = request.environ.get('context')
        try:
            dbapi.cells_delete(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during cell delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None


class CellsData(base.Resource):

    def put(self, id):
        """
        Update existing cell data, or create if it does
        not exist.
        """
        data_keys = request.form.keys()
        data = dict((key, request.form.getlist(key)[0]) for key in data_keys)
        context = request.environ.get('context')
        try:
            dbapi.cells_data_update(context, id, data)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during cell data update: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None

    def delete(self, id):
        """Delete cell data."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        data_keys = request.form.keys()
        data = dict((key, request.form.getlist(key)[0]) for key in data_keys)
        context = request.environ.get('context')
        try:
            dbapi.cells_data_delete(context, id, data)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during cell delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None
