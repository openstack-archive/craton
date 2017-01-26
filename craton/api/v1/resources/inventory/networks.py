from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Networks(base.Resource):
    """Controller for Networks resources."""

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all networks, with optional filtering."""
        networks_obj, link_params = dbapi.networks_get_all(
            context, request_args, pagination_params,
        )
        links = base.links_from(link_params)
        response_body = {'networks': networks_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new network."""
        json = util.copy_project_id_into_json(context, request_data)
        network_obj = dbapi.networks_create(context, json)
        return jsonutils.to_primitive(network_obj), 200, None


class NetworkById(base.Resource):
    """Controller for Networks by ID."""

    @base.http_codes
    def get(self, context, id):
        """Get network by given id"""
        obj = dbapi.networks_get_by_id(context, id)
        device = jsonutils.to_primitive(obj)
        device['variables'] = jsonutils.to_primitive(obj.variables)
        return device, 200, None

    def put(self, context, id, request_data):
        """Update existing network values."""
        net_obj = dbapi.networks_update(context, id, request_data)
        return jsonutils.to_primitive(net_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing network."""
        dbapi.networks_delete(context, id)
        return None, 204, None


class NetworksVariables(base.Resource):
    """Controller for networks variables endpoints."""

    @base.http_codes
    def get(self, context, id):
        """Get variables for the given network."""
        obj = dbapi.networks_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, context, id, request_data):
        """"Update existing variables, or create if it does not exist."""
        obj = dbapi.networks_variables_update(context, id, request_data)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, context, id, request_data):
        """Delete networks variables."""
        dbapi.networks_variables_delete(context, id, request_data)
        return None, 204, None


class NetworkDevices(base.Resource):
    """Controller for Network Device resources."""

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all network devices."""
        devices_obj, link_params = dbapi.network_devices_get_all(
            context, request_args, pagination_params,
        )
        links = base.links_from(link_params)
        response_body = {'network_devices': devices_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new network device."""
        json = util.copy_project_id_into_json(context, request_data)
        obj = dbapi.network_devices_create(context, json)
        device = jsonutils.to_primitive(obj)
        return device, 200, None


class NetworkDeviceById(base.Resource):
    """Controller for Network Devices by ID."""

    @base.http_codes
    def get(self, context, id, request_args):
        """Get network device by given id"""
        resolved_values = request_args["resolved-values"]
        obj = dbapi.network_devices_get_by_id(context, id)
        if resolved_values:
            obj.vars = obj.resolved
        else:
            obj.vars = obj.variables
        device = jsonutils.to_primitive(obj)
        device['variables'] = jsonutils.to_primitive(obj.vars)
        return device, 200, None

    def put(self, context, id, request_data):
        """Update existing device values."""
        net_obj = dbapi.network_devices_update(context, id, request_data)
        return jsonutils.to_primitive(net_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing network device."""
        dbapi.network_devices_delete(context, id)
        return None, 204, None


class NetworkDevicesVariables(base.Resource):
    """Controller for network device variables endpoints."""

    @base.http_codes
    def get(self, context, id):
        """Get variables for the given network."""
        obj = dbapi.network_devices_get_by_id(context, id)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def put(self, context, id, request_data):
        """"Update device variables, or create if it does not exist."""
        obj = dbapi.network_devices_variables_update(context, id, request_data)
        resp = {"variables": jsonutils.to_primitive(obj.variables)}
        return resp, 200, None

    @base.http_codes
    def delete(self, context, id, request_data):
        """Delete network device variables."""
        dbapi.network_devices_variables_delete(context, id, request_data)
        return None, 204, None


class NetworkDeviceLabels(base.Resource):
    """Controller for Netowrk Device Labels."""

    @base.http_codes
    def get(self, context, id):
        """Get labels for given network device."""
        obj = dbapi.network_devices_get_by_id(context, id)
        response = {"labels": list(obj.labels)}
        return response, 200, None

    @base.http_codes
    def put(self, context, id, request_data):
        """Update existing device label. Adds if it does not exist."""
        resp = dbapi.network_devices_labels_update(context, id, request_data)
        response = {"labels": list(resp.labels)}
        return response, 200, None

    @base.http_codes
    def delete(self, context, id, request_data):
        """Delete device label(s)."""
        dbapi.network_devices_labels_delete(context, id, request_data)
        return None, 204, None


class NetworkInterfaces(base.Resource):
    """Controller for Netowrk Interfaces."""

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all network interfaces."""
        interfaces_obj, link_params = dbapi.network_interfaces_get_all(
            context, request_args, pagination_params,
        )
        links = base.links_from(link_params)
        response_body = {'network_interfaces': interfaces_obj, 'links': links}
        return jsonutils.to_primitive(response_body), 200, None

    @base.http_codes
    def post(self, context, request_data):
        """Create a new network interface."""
        json = util.copy_project_id_into_json(context, request_data)
        obj = dbapi.network_interfaces_create(context, json)
        interface = jsonutils.to_primitive(obj)
        return interface, 200, None


class NetworkInterfaceById(base.Resource):

    @base.http_codes
    def get(self, context, id):
        """Get network interface by given id"""
        obj = dbapi.network_interfaces_get_by_id(context, id)
        interface = jsonutils.to_primitive(obj)
        interface['variables'] = jsonutils.to_primitive(obj.variables)
        return interface, 200, None

    def put(self, context, id, request_data):
        """Update existing network interface values."""
        net_obj = dbapi.network_interfaces_update(context, id, request_data)
        return jsonutils.to_primitive(net_obj), 200, None

    @base.http_codes
    def delete(self, context, id):
        """Delete existing network interface."""
        dbapi.network_interfaces_delete(context, id)
        return None, 204, None
