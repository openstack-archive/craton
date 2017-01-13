from flask import g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Hosts(base.Resource):

    @base.http_codes
    @base.filtered_context()
    def get(self, context, **filters):
        """Get all hosts for region, with optional filtering."""
        hosts_obj = dbapi.hosts_get_all(context, filters)
        return jsonutils.to_primitive(hosts_obj), 200, None

    @base.http_codes
    def post(self, context):
        """Create a new host."""
        json = util.copy_project_id_into_json(context, g.json)
        host_obj = dbapi.hosts_create(context, json)
        host = jsonutils.to_primitive(host_obj)
        if 'variables' in json:
            host["variables"] = jsonutils.to_primitive(host_obj.variables)
        else:
            host["variables"] = {}
        return host, 200, None


def format_variables(args, obj):
    resolved_values = args["resolved-values"]
    if resolved_values:
        obj.vars = obj.resolved
    else:
        obj.vars = obj.variables
    return obj


class HostById(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get host by given id"""
        host_obj = dbapi.hosts_get_by_id(context, id)
        host_obj = format_variables(g.args, host_obj)
        host = jsonutils.to_primitive(host_obj)
        host['variables'] = jsonutils.to_primitive(host_obj.vars)
        return host, 200, None

    def put(self, context, id):
        """Update existing host data, or create if it does not exist."""
        host_obj = dbapi.hosts_update(context, id, g.json)
        return jsonutils.to_primitive(host_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing host."""
        dbapi.hosts_delete(context, id)
        return None, 204, None


class HostsVariables(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get variables for given host."""
        obj = dbapi.hosts_get_by_id(context, id)
        obj = format_variables(g.args, obj)
        response = {"variables": jsonutils.to_primitive(obj.vars)}
        return response, 200, None

    @base.http_codes
    def put(self, context, id):
        """Update existing host variables, or create if it does not exist."""
        obj = dbapi.hosts_variables_update(context, id, g.json)
        response = {"variables": jsonutils.to_primitive(obj.variables)}
        return response, 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete host  variables."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        dbapi.hosts_variables_delete(context, id, g.json)
        return None, 204, None


class HostsLabels(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get labels for given host device."""
        host_obj = dbapi.hosts_get_by_id(context, id)
        response = {"labels": list(host_obj.labels)}
        return response, 200, None

    @base.http_codes
    def put(self, context, id):
        """
        Update existing device label entirely, or add if it does
        not exist.
        """
        resp = dbapi.hosts_labels_update(context, id, g.json)
        response = {"labels": list(resp.labels)}
        return response, 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete device label entirely."""
        dbapi.hosts_labels_delete(context, id, g.json)
        return None, 204, None
