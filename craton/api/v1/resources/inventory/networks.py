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
        reserved_keys=['id', 'name', 'cell_id', 'network_type',
                       'region_id', 'vars'])
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
        device = jsonutils.to_primitive(obj)
        device['variables'] = jsonutils.to_primitive(obj.variables)
        return device, 200, None

    def put(self, id):
        """Update existing network values."""
        context = request.environ.get('context')
        net_obj = dbapi.networks_update(context, id, request.json)
        return jsonutils.to_primitive(net_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing network."""
        context = request.environ.get('context')
        dbapi.networks_delete(context, id)
        return None, 204, None


class NetworksVariables(base.Resource):
    """Controller for networks variables endpoints."""

    @base.http_codes
    def get(self, id):
        """Get variables for the given network."""
        context = request.environ.get('context')
        obj = dbapi.networks_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, id):
        """"Update existing variables, or create if it does not exist."""
        context = request.environ.get('context')
        obj = dbapi.networks_variables_update(context, id, request.json)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete networks variables."""
        context = request.environ.get('context')
        dbapi.networks_variables_delete(context, id, request.json)
        return None, 204, None


class NetworkDevices(base.Resource):
    """Controller for Network Device resources."""

    @base.http_codes
    @base.filtered_context(
        required='region_id',
        reserved_keys=['id', 'name', 'ip_address', 'cell_id',
                       'device_type', 'region_id', 'vars'])
    def get(self, context, region_id, filters):
        """Get all network devices for this region."""
        devices_obj = dbapi.network_devices_get_by_region(
            context, region_id, filters)
        return jsonutils.to_primitive(devices_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new network device."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        obj = dbapi.network_devices_create(context, json)
        device = jsonutils.to_primitive(obj)
        return device, 200, None


class NetworkDeviceById(base.Resource):
    """Controller for Network Devices by ID."""

    @base.http_codes
    def get(self, id):
        """Get network device by given id"""
        context = request.environ.get('context')
        resolved_values = g.args["resolved-values"]
        obj = dbapi.network_devices_get_by_id(context, id)
        if resolved_values:
            obj.vars = obj.resolved
        else:
            obj.vars = obj.variables
        device = jsonutils.to_primitive(obj)
        device['variables'] = jsonutils.to_primitive(obj.vars)
        return device, 200, None

    def put(self, id):
        """Update existing device values."""
        context = request.environ.get('context')
        net_obj = dbapi.network_devices_update(context, id, request.json)
        return jsonutils.to_primitive(net_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing network device."""
        context = request.environ.get('context')
        dbapi.network_devices_delete(context, id)
        return None, 204, None


class NetworkDevicesVariables(base.Resource):
    """Controller for network device variables endpoints."""

    @base.http_codes
    def get(self, id):
        """Get variables for the given network."""
        context = request.environ.get('context')
        obj = dbapi.network_devices_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, id):
        """"Update device variables, or create if it does not exist."""
        context = request.environ.get('context')
        obj = dbapi.network_devices_variables_update(context, id, request.json)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete network device variables."""
        context = request.environ.get('context')
        dbapi.network_devices_variables_delete(context, id, request.json)
        return None, 204, None


class NetworkDeviceLabels(base.Resource):
    """Controller for Netowrk Device Labels."""

    @base.http_codes
    def get(self, id):
        """Get labels for given network device."""
        context = request.environ.get('context')
        obj = dbapi.network_devices_get_by_id(context, id)
        response = {"labels": list(obj.labels)}
        return response, 200, None

    @base.http_codes
    def put(self, id):
        """Update existing device label. Adds if it does not exist."""
        context = request.environ.get('context')
        resp = dbapi.network_devices_labels_update(context, id, request.json)
        response = {"labels": list(resp.labels)}
        return response, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete device label(s)."""
        context = request.environ.get('context')
        dbapi.network_devices_labels_delete(context, id)
        return None, 204, None


class NetworkInterfaces(base.Resource):
    """Controller for Netowrk Interfaces."""

    @base.http_codes
    @base.filtered_context(
        required='device_id',
        reserved_keys=['id', 'ip_address', 'interface_type',
                       'device_id', 'vars'])
    def get(self, context, device_id, filters):
        """Get all network interfaces for a given network device."""
        interfaces_obj = dbapi.network_interfaces_get_by_device(
            context, device_id, filters)
        return jsonutils.to_primitive(interfaces_obj), 200, None

    @base.http_codes
    def post(self):
        """Create a new network interface."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        obj = dbapi.network_interfaces_create(context, json)
        interface = jsonutils.to_primitive(obj)
        return interface, 200, None


class NetworkInterfaceById(base.Resource):

    @base.http_codes
    def get(self, id):
        """Get network interface by given id"""
        context = request.environ.get('context')
        obj = dbapi.network_interfaces_get_by_id(context, id)
        interface = jsonutils.to_primitive(obj)
        interface['variables'] = jsonutils.to_primitive(obj.variables)
        return interface, 200, None

    def put(self, id):
        """Update existing network interface values."""
        context = request.environ.get('context')
        net_obj = dbapi.network_interfaces_update(context, id, request.json)
        return jsonutils.to_primitive(net_obj), 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing network interface."""
        context = request.environ.get('context')
        dbapi.network_interfaces_delete(context, id)
        return None, 203, None
