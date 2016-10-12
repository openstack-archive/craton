from flask import g
from flask import request
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi


LOG = log.getLogger(__name__)


class Hosts(base.Resource):

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        filters=['id', 'name', 'ip_address', 'cell_id', 'device_type'])
    def get(self, context, region_id, filters):
        """Get all hosts for region, with optional filtering."""
        hosts_obj = dbapi.hosts_get_by_region(context, region_id, filters)
        return jsonutils.to_primitive(hosts_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new host."""
        context = request.environ.get('context')
        host_obj = dbapi.hosts_create(context, g.json)
        return jsonutils.to_primitive(host_obj), 200, None


class HostById(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get host by given id"""
        context = request.environ.get('context')
        resolved_values = g.args["resolved-values"]
        host_obj = dbapi.hosts_get_by_id(context, id)
        if resolved_values:
            host_obj.data = host_obj.resolved
        else:
            host_obj.data = host_obj.variables
        host_obj.labels = host_obj.labels
        host = jsonutils.to_primitive(host_obj)
        return host, 200, None

    def put(self, id):
        return None, 400, None

    @base.http_codes
    def delete(self, id):
        """Delete existing host."""
        context = request.environ.get('context')
        dbapi.hosts_delete(context, id)
        return None, 204, None


class HostsData(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get data for given host."""
        context = request.environ.get('context')
        obj = dbapi.hosts_get_by_id(context, id)
        response = {"data": jsonutils.to_primitive(obj.variables)}
        return response, 200, None

    @base.http_codes
    def put(self, id):
        """
        Update existing host data, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        obj = dbapi.hosts_data_update(context, id, request.json)
        response = {"data": jsonutils.to_primitive(obj.variables)}
        return response, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete host  data."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        context = request.environ.get('context')
        dbapi.hosts_data_delete(context, id, request.json)
        return None, 204, None


class HostsLabels(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get labels for given host device."""
        context = request.environ.get('context')
        host_obj = dbapi.hosts_get_by_id(context, id)
        response = {"labels": list(host_obj.labels)}
        return response, 200, None

    @base.http_codes
    def put(self, id):
        """
        Update existing device label entirely, or add if it does
        not exist.
        """
        context = request.environ.get('context')
        resp = dbapi.hosts_labels_update(context, id, request.json)
        response = {"labels": list(resp)}
        return response, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete device label entirely."""
        context = request.environ.get('context')
        dbapi.hosts_labels_delete(context, id, request.json)
        return None, 204, None
