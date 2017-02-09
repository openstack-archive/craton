from oslo_serialization import jsonutils
from oslo_log import log

from craton.api import v1
from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Cells(base.Resource):

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all cells, with optional filtering."""
        cells_obj = dbapi.cells_get_all(
            context, request_args, pagination_params,
        )
        return jsonutils.to_primitive(cells_obj), 200, None

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

        location = v1.api.url_for(
            CellById, id=cell_obj.id, _external=True
        )
        headers = {'Location': location}

        return cell, 201, headers


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
