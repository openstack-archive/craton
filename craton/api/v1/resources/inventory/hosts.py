from flask import g
from flask import request
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Hosts(base.Resource):

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        reserved_keys=['id', 'name', 'ip_address', 'cell_id', 'vars',
                       'device_type', 'label', 'limit', 'region_id'])
    def get(self, context, region_id, filters):
        """Get all hosts for region, with optional filtering."""
        hosts_obj = dbapi.hosts_get_by_region(context, region_id, filters)
        return jsonutils.to_primitive(hosts_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new host."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        host_obj = dbapi.hosts_create(context, json)
        return jsonutils.to_primitive(host_obj), 200, None


def format_variables(args, obj):
    resolved_values = args["resolved-values"]
    if resolved_values:
        obj.vars = obj.resolved
    else:
        obj.vars = obj.variables
    return obj


class HostById(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get host by given id"""
        context = request.environ.get('context')
        host_obj = dbapi.hosts_get_by_id(context, id)
        host_obj = format_variables(g.args, host_obj)
        host = jsonutils.to_primitive(host_obj)
        host['variables'] = jsonutils.to_primitive(host_obj.vars)
        return host, 200, None

    def put(self, id):
        """Update existing host data, or create if it does not exist."""
        context = request.environ.get('context')
        host_obj = dbapi.hosts_update(context, id, request.json)
        return jsonutils.to_primitive(host_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing host."""
        context = request.environ.get('context')
        dbapi.hosts_delete(context, id)
        return None, 204, None


class HostsVariables(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get variables for given host."""
        context = request.environ.get('context')
        obj = dbapi.hosts_get_by_id(context, id)
        obj = format_variables(g.args, obj)
        response = {"variables": jsonutils.to_primitive(obj.vars)}
        return response, 200, None

    @base.http_codes
    def put(self, id):
        """Update existing host variables, or create if it does not exist."""
        context = request.environ.get('context')
        obj = dbapi.hosts_variables_update(context, id, request.json)
        response = {"variables": jsonutils.to_primitive(obj.variables)}
        return response, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete host  variables."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        context = request.environ.get('context')
        dbapi.hosts_variables_delete(context, id, request.json)
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
        response = {"labels": list(resp.labels)}
        return response, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete device label entirely."""
        context = request.environ.get('context')
        dbapi.hosts_labels_delete(context, id, request.json)
        return None, 204, None
