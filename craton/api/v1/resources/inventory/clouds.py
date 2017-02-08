from oslo_serialization import jsonutils
from oslo_log import log

from craton.api import v1
from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Clouds(base.Resource):

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get cloud(s) for the project. Get cloud details if
        for a particular cloud.
        """
        cloud_id = request_args.get("id")
        cloud_name = request_args.get("name")

        if not (cloud_id or cloud_name):
            # Get all clouds for this tenant
            clouds_obj, link_params = dbapi.clouds_get_all(
                context, request_args, pagination_params,
            )
        else:
            if cloud_name:
                cloud_obj = dbapi.clouds_get_by_name(context, cloud_name)
                cloud_obj.data = cloud_obj.variables

            if cloud_id:
                cloud_obj = dbapi.clouds_get_by_id(context, cloud_id)
                cloud_obj.data = cloud_obj.variables

            clouds_obj = [cloud_obj]
            link_params = {}
        links = base.links_from(link_params)
        response_body = {'clouds': clouds_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new cloud."""
        json = util.copy_project_id_into_json(context, request_data)
        cloud_obj = dbapi.clouds_create(context, json)
        cloud = jsonutils.to_primitive(cloud_obj)
        if 'variables' in json:
            cloud["variables"] = jsonutils.to_primitive(cloud_obj.variables)
        else:
            cloud["variables"] = {}

        location = v1.api.url_for(
            CloudsById, id=cloud_obj.id, _external=True
        )
        headers = {'Location': location}

        return cloud, 201, headers


class CloudsById(base.Resource):

    @base.http_codes
    def get(self, context, id):
        cloud_obj = dbapi.clouds_get_by_id(context, id)
        cloud = jsonutils.to_primitive(cloud_obj)
        cloud['variables'] = jsonutils.to_primitive(cloud_obj.variables)
        return cloud, 200, None

    def put(self, context, id, request_data):
        """Update existing cloud."""
        cloud_obj = dbapi.clouds_update(context, id, request_data)
        return jsonutils.to_primitive(cloud_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing cloud."""
        dbapi.clouds_delete(context, id)
        return None, 204, None
