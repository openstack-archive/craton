from flask import g
from flask import request
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Hosts(base.Resource):

    def get(self):
        """
        Get all hosts for region/cell. You can get hosts for
        a particular region or for a region/cell combination.

        :param region: Region this host belongs to (required)
        :param cell: Cell this host belongs to
        :param name: Name of the host to get
        :param id: ID of the host to get
        :param ip_address: IP address of the host to get
        """
        region = g.args["region"]
        cell = g.args["cell"]
        name = g.args["name"]
        host_id = g.args["id"]
        device_type = g.args["device_type"]
        ip_address = g.args["ip"]

        context = request.environ.get("context")

        filters = {}
        if host_id:
            filters["id"] = host_id
        if name:
            filters["name"] = name
        if ip_address:
            filters["ip_address"] = ip_address
        if cell:
            filters["cell"] = cell
        if device_type:
            filters["device_type"] = device_type

        # This is a query constraint, you can't fetch all hosts
        # for all regions, you have to query hosts by region.
        if not region:
            return self.error_response(400, "Missing `region` in query")

        try:
            LOG.info("Getting hosts that match filters %s" % filters)
            hosts_obj = dbapi.hosts_get_by_region(context, region, filters)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during host get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        hosts = jsonutils.to_primitive(hosts_obj)
        return hosts, 200, None

    def post(self):
        """Create a new host."""
        context = request.environ.get('context')
        try:
            host_obj = dbapi.hosts_create(context, g.json)
        except Exception as err:
            LOG.error("Error during host create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        host = jsonutils.to_primitive(host_obj)
        return host, 200, None


class HostById(base.Resource):

    def get(self, id):
        """Get host by given id"""
        context = request.environ.get('context')
        resolved_values = g.args["resolved-values"]

        try:
            host_obj = dbapi.hosts_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during host get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        if resolved_values:
            host_obj.data = host_obj.resolved
        else:
            host_obj.data = host_obj.variables

        host_obj.labels = host_obj.labels
        host = jsonutils.to_primitive(host_obj)
        return host, 200, None

    def put(self, id):
        return None, 400, None

    def delete(self, id):
        """Delete existing host."""
        context = request.environ.get('context')
        try:
            dbapi.hosts_delete(context, id)
        except Exception as err:
            LOG.error("Error during host delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None


class HostsData(base.Resource):

    def put(self, id):
        """
        Update existing host data, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        try:
            dbapi.hosts_data_update(context, id, request.json)
        except Exception as err:
            LOG.error("Error during host data update: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None

    def delete(self, id):
        """Delete host  data."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        context = request.environ.get('context')
        try:
            dbapi.hosts_data_delete(context, id, request.json)
        except Exception as err:
            LOG.error("Error during host delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None
