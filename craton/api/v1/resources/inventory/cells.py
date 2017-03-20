from oslo_serialization import jsonutils
from oslo_log import log

from craton.api import v1
from craton.api.v1 import base
from craton.api.v1.resources import utils
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Cells(base.Resource):

    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all cells, with optional filtering."""
        details = request_args.get("details")

        cells_obj, link_params = dbapi.cells_get_all(
            context, request_args, pagination_params,
        )
        if details:
            cells_obj = [utils.get_resource_with_vars(request_args, cell)
                         for cell in cells_obj]

        links = base.links_from(link_params)
        response_body = {'cells': cells_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

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

    def get(self, context, id, request_args):
        cell_obj = dbapi.cells_get_by_id(context, id)
        cell = utils.get_resource_with_vars(request_args, cell_obj)
        return cell, 200, None

    def put(self, context, id, request_data):
        """Update existing cell."""
        cell_obj = dbapi.cells_update(context, id, request_data)
        return jsonutils.to_primitive(cell_obj), 200, None

    def delete(self, context, id):
        """Delete existing cell."""
        dbapi.cells_delete(context, id)
        return None, 204, None
