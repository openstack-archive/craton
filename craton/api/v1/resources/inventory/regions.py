from oslo_serialization import jsonutils
from oslo_log import log

from craton.api import v1
from craton.api.v1 import base
from craton.api.v1.resources import utils
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Regions(base.Resource):

    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get region(s) for the project. Get region details if
        for a particular region.
        """
        region_id = request_args.get("id")
        region_name = request_args.get("name")
        details = request_args.get("details")

        if not (region_id or region_name):
            # Get all regions for this tenant
            regions_obj, link_params = dbapi.regions_get_all(
                context, request_args, pagination_params,
            )
            if details:
                regions_obj = [utils.get_resource_with_vars(request_args, r)
                               for r in regions_obj]
        else:
            if region_name:
                region_obj = dbapi.regions_get_by_name(context, region_name)
                region_obj.data = region_obj.variables

            if region_id:
                region_obj = dbapi.regions_get_by_id(context, region_id)
                region_obj.data = region_obj.variables

            regions_obj = [region_obj]
            link_params = {}
        links = base.links_from(link_params)
        response_body = {'regions': regions_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    def post(self, context, request_data):
        """Create a new region."""
        json = util.copy_project_id_into_json(context, request_data)
        region_obj = dbapi.regions_create(context, json)
        region = jsonutils.to_primitive(region_obj)
        if 'variables' in json:
            region["variables"] = jsonutils.to_primitive(region_obj.variables)
        else:
            region["variables"] = {}

        location = v1.api.url_for(
            RegionsById, id=region_obj.id, _external=True
        )
        headers = {'Location': location}

        return region, 201, headers


class RegionsById(base.Resource):

    def get(self, context, id, request_args):
        region_obj = dbapi.regions_get_by_id(context, id)
        region = utils.get_resource_with_vars(request_args, region_obj)
        return region, 200, None

    def put(self, context, id, request_data):
        """Update existing region."""
        region_obj = dbapi.regions_update(context, id, request_data)
        return jsonutils.to_primitive(region_obj), 200, None

    def delete(self, context, id):
        """Delete existing region."""
        dbapi.regions_delete(context, id)
        return None, 204, None
