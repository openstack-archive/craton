from copy import deepcopy

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base


class VariablesDBTestCase:
    project_id = "5a4e32e1-8571-4c2c-a088-a11f98900355"

    def create_region(self, name, variables=None):
        region = dbapi.regions_create(
            self.context,
            {
                'name': name,
                'project_id': self.project_id,
                'variables': variables or {},
            },
        )
        return region.id

    def create_cell(self, name, region_id, variables=None):
        cell = dbapi.cells_create(
            self.context,
            {
                'name': name,
                'project_id': self.project_id,
                'region_id': region_id,
                'variables': variables or {}
            },
        )
        return cell.id

    def create_host(
            self, name, region_id, ip_address, host_type, cell_id=None,
            parent_id=None, labels=None, variables=None,
            ):
        host = {
            'name': name,
            'project_id': self.project_id,
            'region_id': region_id,
            'cell_id': cell_id,
            'ip_address': ip_address,
            'parent_id': parent_id,
            'device_type': host_type,
            'active': True,
            'labels': labels or (),
            'variables': variables or {},
        }

        host = dbapi.hosts_create(self.context, host)
        self.assertEqual(variables, host.variables)

        return host.id

    def create_network(
            self, name, region_id, cidr, gateway, netmask, cell_id=None,
            variables=None,
            ):
        network = {
            'name': name,
            'project_id': self.project_id,
            'region_id': region_id,
            'cell_id': cell_id,
            'cidr': cidr,
            'gateway': gateway,
            'netmask': netmask,
            'variables': variables or {},
        }

        network = dbapi.networks_create(self.context, network)
        self.assertEqual(variables, network.variables)

        return network.id

    def create_network_device(
            self, name, region_id, ip_address, network_device_type,
            cell_id=None, parent_id=None, labels=None, variables=None,
            ):
        network_device = {
            'name': name,
            'project_id': self.project_id,
            'region_id': region_id,
            'cell_id': cell_id,
            'ip_address': ip_address,
            'parent_id': parent_id,
            'device_type': network_device_type,
            'active': True,
            'labels': labels or (),
            'variables': variables or {},
        }

        network_device = dbapi.network_devices_create(
            self.context, network_device
        )
        self.assertEqual(variables, network_device.variables)

        return network_device.id

    def setup_host(self, variables):
        region_id = self.create_region(name='region1')
        cell_id = self.create_cell(name="cell1", region_id=region_id)
        host_id = self.create_host(
            name="host1",
            region_id=region_id,
            ip_address="192.168.2.1",
            host_type="server",
            cell_id=cell_id,
            parent_id=None,
            labels=None,
            variables=variables,
        )

        return host_id

    def setup_network_device(self, variables):
        region_id = self.create_region(name='region1')
        cell_id = self.create_cell(name="cell1", region_id=region_id)
        network_device_id = self.create_network_device(
            name="network_device1",
            region_id=region_id,
            ip_address="192.168.2.1",
            network_device_type="switch",
            cell_id=cell_id,
            parent_id=None,
            labels=None,
            variables=variables,
        )

        return network_device_id

    def setup_network(self, variables):
        region_id = self.create_region(name='region1')
        cell_id = self.create_cell(name="cell1", region_id=region_id)
        network_id = self.create_network(
            name="network1",
            region_id=region_id,
            cell_id=cell_id,
            cidr="192.168.2.0/24",
            gateway="192.168.2.1",
            netmask="255.255.255.0",
            variables=variables,
        )

        return network_id

    def setup_cell(self, variables):
        region_id = self.create_region(name='region1')
        cell_id = self.create_cell(
            name="cell1",
            region_id=region_id,
            variables=variables,
        )

        return cell_id

    def setup_region(self, variables):
        region_id = self.create_region(
            name='region1',
            variables=variables,
        )

        return region_id

    def setup_resource(self, *args, **kwargs):
        setup_fn = {
            "cells": self.setup_cell,
            "hosts": self.setup_host,
            "networks": self.setup_network,
            "network-devices": self.setup_network_device,
            "regions": self.setup_region,
        }

        return setup_fn[self.resources_type](*args, *kwargs)

    def test_get_resource_by_id_with_variables(self):
        variables = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        resource_id = self.setup_resource(deepcopy(variables))

        test = dbapi.resource_get_by_id(
            self.context, self.resources_type, resource_id
        )

        self.assertEqual(resource_id, test.id)
        self.assertEqual(variables, test.variables)

    def test_get_resource_by_id_not_found(self):

        self.assertRaises(
            exceptions.NotFound,
            dbapi.resource_get_by_id,
            context=self.context,
            resources=self.resources_type,
            resource_id=1,
        )

    def test_variables_update_by_resource_id_existing_empty(self):
        existing_variables = {}

        resource_id = self.setup_resource(existing_variables)

        variables = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        test = dbapi.variables_update_by_resource_id(
            self.context, self.resources_type, resource_id, deepcopy(variables)
        )

        self.assertEqual(resource_id, test.id)
        self.assertEqual(variables, test.variables)

        validate = dbapi.resource_get_by_id(
            self.context, self.resources_type, resource_id
        )

        self.assertEqual(resource_id, validate.id)
        self.assertEqual(variables, validate.variables)

    def test_variables_update_by_resource_id_not_found(self):

        self.assertRaises(
            exceptions.NotFound,
            dbapi.variables_update_by_resource_id,
            context=self.context,
            resources=self.resources_type,
            resource_id=1,
            data={"key1": "value1"},
        )

    def test_variables_update_by_resource_id_modify_existing(self):
        existing_variables = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        update_variables = {
            "key3": "newvalue3",
            "key4": "value4",
        }

        result_variables = deepcopy(existing_variables)
        result_variables.update(deepcopy(update_variables))

        resource_id = self.setup_resource(existing_variables)

        test = dbapi.variables_update_by_resource_id(
            context=self.context,
            resources=self.resources_type,
            resource_id=resource_id,
            data=deepcopy(update_variables)
        )

        self.assertEqual(resource_id, test.id)
        self.assertEqual(result_variables, test.variables)

        validate = dbapi.resource_get_by_id(
            self.context, self.resources_type, resource_id
        )

        self.assertEqual(resource_id, validate.id)
        self.assertEqual(result_variables, validate.variables)

    def test_variables_delete_by_resource_id(self):
        existing_variables = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        delete_variables = {
            "_": "key2",
            "foo": "key3",
        }

        result_variables = {"key1": "value1"}

        resource_id = self.setup_resource(existing_variables)

        test = dbapi.variables_delete_by_resource_id(
            context=self.context,
            resources=self.resources_type,
            resource_id=resource_id,
            data=delete_variables
        )

        self.assertEqual(resource_id, test.id)
        self.assertEqual(result_variables, test.variables)

        validate = dbapi.resource_get_by_id(
            self.context, self.resources_type, resource_id
        )

        self.assertEqual(resource_id, validate.id)
        self.assertEqual(result_variables, validate.variables)

    def test_variables_delete_by_resource_id_resource_not_found(self):

        self.assertRaises(
            exceptions.NotFound,
            dbapi.variables_delete_by_resource_id,
            context=self.context,
            resources=self.resources_type,
            resource_id=1,
            data={"key1": "value1"},
        )

    def test_variables_delete_by_resource_id_variable_not_found(self):
        existing_variables = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        delete_variables = {
            "_": "key4",
        }

        result_variables = deepcopy(existing_variables)

        resource_id = self.setup_resource(existing_variables)

        test = dbapi.variables_delete_by_resource_id(
            context=self.context,
            resources=self.resources_type,
            resource_id=resource_id,
            data=delete_variables
        )

        self.assertEqual(resource_id, test.id)
        self.assertEqual(result_variables, test.variables)

        validate = dbapi.resource_get_by_id(
            self.context, self.resources_type, resource_id
        )

        self.assertEqual(resource_id, validate.id)
        self.assertEqual(result_variables, validate.variables)


class HostsVariablesDBTestCase(VariablesDBTestCase, base.DBTestCase):
    resources_type = "hosts"


class NetworkDevicesVariablesDBTestCase(VariablesDBTestCase, base.DBTestCase):
    resources_type = "network-devices"


class CellsVariablesDBTestCase(VariablesDBTestCase, base.DBTestCase):
    resources_type = "cells"


class RegionsVariablesDBTestCase(VariablesDBTestCase, base.DBTestCase):
    resources_type = "regions"


class NetworksVariablesDBTestCase(VariablesDBTestCase, base.DBTestCase):
    resources_type = "networks"
