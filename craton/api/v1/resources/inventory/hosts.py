from oslo_serialization import jsonutils
from oslo_log import log

from craton.api import v1
from craton.api.v1 import base
from craton.api.v1.resources import utils
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Hosts(base.Resource):

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all hosts for region, with optional filtering."""
        hosts_obj, link_params = dbapi.hosts_get_all(
            context, request_args, pagination_params,
        )
        links = base.links_from(link_params)
        response_body = {'hosts': hosts_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new host."""
        json = util.copy_project_id_into_json(context, request_data)
        host_obj = dbapi.hosts_create(context, json)
        host = jsonutils.to_primitive(host_obj)
        if 'variables' in json:
            host["variables"] = jsonutils.to_primitive(host_obj.variables)
        else:
            host["variables"] = {}

        location = v1.api.url_for(
            HostById, id=host_obj.id, _external=True
        )
        headers = {'Location': location}

        return host, 201, headers


class HostById(base.Resource):

    @base.http_codes
    def get(self, context, id, request_args):
        """Get host by given id"""
        host_obj = dbapi.hosts_get_by_id(context, id)
        host_obj = utils.format_variables(request_args, host_obj)
        host = jsonutils.to_primitive(host_obj)
        host['variables'] = jsonutils.to_primitive(host_obj.vars)
        return host, 200, None

    def put(self, context, id, request_data):
        """Update existing host data, or create if it does not exist."""
        host_obj = dbapi.hosts_update(context, id, request_data)
        return jsonutils.to_primitive(host_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing host."""
        dbapi.hosts_delete(context, id)
        return None, 204, None


class HostsLabels(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get labels for given host device."""
        host_obj = dbapi.hosts_get_by_id(context, id)
        response = {"labels": list(host_obj.labels)}
        return response, 200, None

    @base.http_codes
    def put(self, context, id, request_data):
        """
        Update existing device label entirely, or add if it does
        not exist.
        """
        resp = dbapi.hosts_labels_update(context, id, request_data)
        response = {"labels": list(resp.labels)}
        return response, 200, None

    @base.http_codes
    def delete(self, context, id, request_data):
        """Delete device label entirely."""
        dbapi.hosts_labels_delete(context, id, request_data)
        return None, 204, None
