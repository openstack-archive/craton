from flask import g
from flask import request
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Networks(base.Resource):
    """Controller for Netowrks resources."""

    def get(self):
        """Get all networks for this cell/region."""
        id = g.args["id"]
        region_id = g.args["region"]
        cell_id = g.args["cell"]
        name = g.args["name"]
        network_type = g.args["network_type"]
        context = request.environ.get("context")

        filters = {}
        if id:
            filters["id"] = id
        if name:
            filters["name"] = name
        if cell_id:
            filters["cell_id"] = cell_id
        if network_type:
            filters["network_type"] = network_type

        if not region_id:
            return self.error_response(400, "Missing `region_id` in query")

        try:
            LOG.info("Getting all networks that match filters %s" % filters)
            obj = dbapi.networks_get_by_region(context, region_id, filters)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during networks get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        networks = jsonutils.to_primitive(obj)
        return networks, 200, None

    def post(self):
        """Create a new network."""
        context = request.environ.get('context')
        try:
            obj = dbapi.networks_create(context, g.json)
        except Exception as err:
            LOG.error("Error during network create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        network = jsonutils.to_primitive(obj)
        return network, 200, None


class NetworkById(base.Resource):
    """Controller for Networks by ID."""

    def get(self, id):
        """Get network by given id"""
        context = request.environ.get('context')

        try:
            obj = dbapi.networks_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during net device get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        obj.data = obj.variables
        device = jsonutils.to_primitive(obj)
        return device, 200, None

    def put(self, id):
        """Update existing network values."""
        return None, 400, None

    def delete(self, id):
        """Delete existing network."""
        context = request.environ.get('context')
        try:
            dbapi.networks_delete(context, id)
        except Exception as err:
            LOG.error("Error during net device delete: %s" % err)
            return self.error_response(500, 'Unknown Error')
        return None, 200, None


class NetDevices(base.Resource):
    """Controller for Network Device resources."""

    def get(self):
        """Get all network devices for this cell/region."""
        region_id = g.args["region"]
        cell_id = g.args["cell"]
        name = g.args["name"]
        id = g.args["id"]
        ip_address = g.args["ip"]
        device_type = g.args["device_type"]

        context = request.environ.get("context")

        filters = {}
        if id:
            filters["id"] = id
        if name:
            filters["name"] = name
        if ip_address:
            filters["ip_address"] = ip_address
        if cell_id:
            filters["cell_id"] = cell_id
        if device_type:
            filters["device_type"] = device_type

        if not region_id:
            return self.error_response(400, "Missing `region_id` in query")

        try:
            LOG.info("Getting all network devices that match filters %s"
                     % filters)
            obj = dbapi.netdevices_get_by_region(context, region_id, filters)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during net devices get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        devices = jsonutils.to_primitive(obj)
        return devices, 200, None

    def post(self):
        """Create a new network device."""
        context = request.environ.get('context')
        try:
            obj = dbapi.netdevices_create(context, g.json)
        except Exception as err:
            LOG.error("Error during net device create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        device = jsonutils.to_primitive(obj)
        return device, 200, None


class NetDeviceById(base.Resource):
    """Controller for Network Devices by ID."""

    def get(self, id):
        """Get network device by given id"""
        context = request.environ.get('context')
        resolved_values = g.args["resolved-values"]

        try:
            obj = dbapi.netdevices_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during net device get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        if resolved_values:
            obj.data = obj.resolved
        else:
            obj.data = obj.variables

        obj.labels = obj.labels
        device = jsonutils.to_primitive(obj)
        return device, 200, None

    def put(self, id):
        """Update existing device values."""
        return None, 400, None

    def delete(self, id):
        """Delete existing network device."""
        context = request.environ.get('context')
        try:
            dbapi.netdevices_delete(context, id)
        except Exception as err:
            LOG.error("Error during net device delete: %s" % err)
            return self.error_response(500, 'Unknown Error')
        return None, 200, None


class NetInterfaces(base.Resource):
    """Controller for Netowrk Interfaces."""

    def get(self):
        """Get all network interfaces for a given network device."""
        device_id = g.args["device"]
        id = g.args["id"]
        ip_address = g.args["ip"]
        interface_type = g.args["interface_type"]
        context = request.environ.get("context")

        filters = {}
        if id:
            filters["id"] = id
        if ip_address:
            filters["ip_address"] = ip_address
        if interface_type:
            filters["interface_type"] = interface_type

        # Can only get interfaces for a particular host
        if not device_id:
            return self.error_response(400, "Missing `device_id` in query")

        try:
            LOG.info("Getting all network interface that match filters %s"
                     % filters)
            obj = dbapi.net_interfaces_get_by_device(context,
                                                     device_id,
                                                     filters)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during net interface get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        interfaces = jsonutils.to_primitive(obj)
        return interfaces, 200, None

    def post(self):
        """Create a new network interface."""
        context = request.environ.get('context')
        try:
            obj = dbapi.net_interfaces_create(context, g.json)
        except Exception as err:
            LOG.error("Error during net interface create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        interface = jsonutils.to_primitive(obj)
        return interface, 200, None


class NetInterfaceById(base.Resource):

    def get(self, id):
        """Get network interface by given id"""
        context = request.environ.get('context')

        try:
            obj = dbapi.net_interface_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during net interface get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        obj.data = obj.variables
        obj.labels = obj.labels
        interface = jsonutils.to_primitive(obj)
        return interface, 200, None

    def put(self, id):
        """Update existing network interface values."""
        return None, 400, None

    def delete(self, id):
        """Delete existing network interface."""
        context = request.environ.get('context')
        try:
            dbapi.net_interfaces_delete(context, id)
        except Exception as err:
            LOG.error("Error during net interface delete: %s" % err)
            return self.error_response(500, 'Unknown Error')
        return None, 200, None
