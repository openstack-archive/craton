from flask import g
from flask import request
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Networks(base.Resource):
    """Controller for Networks resources."""

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        filters=['id', 'name', 'cell_id', 'network_type'])
    def get(self, context, region_id, filters):
        """Get all networks for this region, with optional filtering."""
        networks_obj = dbapi.networks_get_by_region(
            context, region_id, filters)
        return jsonutils.to_primitive(networks_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new network."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        network_obj = dbapi.networks_create(context, json)
        return jsonutils.to_primitive(network_obj), 200, None


class NetworkById(base.Resource):
    """Controller for Networks by ID."""

    @base.http_codes
    def get(self, id):
        """Get network by given id"""
        context = request.environ.get('context')
        obj = dbapi.networks_get_by_id(context, id)
        obj.data = obj.variables
        device = jsonutils.to_primitive(obj)
        return device, 200, None

    def put(self, id):
        """Update existing network values."""
        return None, 400, None

    @base.http_codes
    def delete(self, id):
        """Delete existing network."""
        context = request.environ.get('context')
        dbapi.networks_delete(context, id)
        return None, 204, None


class NetDevices(base.Resource):
    """Controller for Network Device resources."""

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        filters=['id', 'name', 'ip_address', 'cell_id', 'device_type'])
    def get(self, context, region_id, filters):
        """Get all network devices for this region."""
        devices_obj = dbapi.netdevices_get_by_region(
            context, region_id, filters)
        return jsonutils.to_primitive(devices_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new network device."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        obj = dbapi.netdevices_create(context, json)
        device = jsonutils.to_primitive(obj)
        return device, 200, None


class NetDeviceById(base.Resource):
    """Controller for Network Devices by ID."""

    @base.http_codes
    def get(self, id):
        """Get network device by given id"""
        context = request.environ.get('context')
        resolved_values = g.args["resolved-values"]
        obj = dbapi.netdevices_get_by_id(context, id)
        if resolved_values:
            obj.data = obj.resolved
        else:
            obj.data = obj.variables
        device = jsonutils.to_primitive(obj)
        return device, 200, None

    def put(self, id):
        """Update existing device values."""
        return None, 400, None

    @base.http_codes
    def delete(self, id):
        """Delete existing network device."""
        context = request.environ.get('context')
        dbapi.netdevices_delete(context, id)
        return None, 204, None


class NetInterfaces(base.Resource):
    """Controller for Netowrk Interfaces."""

    @base.http_codes
    @base.filtered_context(
        required='device_id',
        filters=['id', 'ip_address', 'interface_type'])
    def get(self, context, device_id, filters):
        """Get all network interfaces for a given network device."""
        interfaces_obj = dbapi.net_interfaces_get_by_device(
            context, device_id, filters)
        return jsonutils.to_primitive(interfaces_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new network interface."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        obj = dbapi.net_interfaces_create(context, json)
        interface = jsonutils.to_primitive(obj)
        return interface, 200, None


class NetInterfaceById(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get network interface by given id"""
        context = request.environ.get('context')
        obj = dbapi.net_interface_get_by_id(context, id)
        obj.data = obj.variables
        interface = jsonutils.to_primitive(obj)
        return interface, 200, None

    def put(self, id):
        """Update existing network interface values."""
        return None, 400, None

    @base.http_codes
    def delete(self, id):
        """Delete existing network interface."""
        context = request.environ.get('context')
        dbapi.net_interfaces_delete(context, id)
        return None, 204, None
