import uuid

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base


default_pagination = {'limit': 30, 'marker': None}

project_id1 = uuid.uuid4().hex
network1 = {"name": "test network",
            "cidr": "192.168.1.0/24",
            "gateway": "192.168.1.1",
            "netmask": "255.255.255.0",
            "region_id": 1,
            "project_id": project_id1}

network2 = {"name": "test network2",
            "cidr": "192.168.1.0/24",
            "gateway": "192.168.1.1",
            "netmask": "255.255.255.0",
            "region_id": 2,
            "project_id": project_id1}

device1 = {"hostname": "switch1",
           "model_name": "Model-X",
           "region_id": 1,
           "project_id": project_id1,
           "device_type": "switch",
           "ip_address": "192.168.1.1"}

device2 = {"hostname": "switch2",
           "model_name": "Model-X",
           "region_id": 2,
           "project_id": project_id1,
           "device_type": "switch",
           "ip_address": "192.168.1.1"}

device3 = {"hostname": "foo1",
           "model_name": "Model-Bar",
           "region_id": 1,
           "project_id": project_id1,
           "device_type": "foo",
           "ip_address": "192.168.1.2"}

network_interface1 = {"device_id": 1,
                      "project_id": project_id1,
                      "name": "eth1",
                      "ip_address": "192.168.0.2",
                      "interface_type": "ethernet"}

network_interface2 = {"device_id": 2,
                      "project_id": project_id1,
                      "name": "eth1",
                      "ip_address": "192.168.0.3",
                      "interface_type": "ethernet"}


class NetworksDBTestCase(base.DBTestCase):

    def test_networks_create(self):
        try:
            dbapi.networks_create(self.context, network1)
        except Exception:
            self.fail("Networks create raised unexpected exception")

    def test_network_create_duplicate_name_raises(self):
        dbapi.networks_create(self.context, network1)
        self.assertRaises(exceptions.DuplicateNetwork, dbapi.networks_create,
                          self.context, network1)

    def test_networks_get_all(self):
        dbapi.networks_create(self.context, network1)
        dbapi.networks_create(self.context, network2)
        filters = {}
        res = dbapi.networks_get_all(self.context, filters,
                                     default_pagination)
        self.assertEqual(len(res), 2)

    def test_networks_get_all_filter_region(self):
        dbapi.networks_create(self.context, network1)
        dbapi.networks_create(self.context, network2)
        filters = {
            'region_id': network1['region_id'],
        }
        res = dbapi.networks_get_all(self.context, filters,
                                     default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'test network')

    def test_networks_get_by_id(self):
        network = dbapi.networks_create(self.context, network1)
        res = dbapi.networks_get_by_id(self.context, network.id)
        self.assertEqual(res.name, 'test network')

    def test_networks_get_by_name_filter_no_exit(self):
        dbapi.networks_create(self.context, network1)
        filters = {"name": "foo", "region_id": network1['region_id']}
        res = dbapi.networks_get_all(self.context, filters,
                                     default_pagination)
        self.assertEqual(res, [])

    def test_network_update(self):
        network = dbapi.networks_create(self.context, network1)
        res = dbapi.networks_get_by_id(self.context, network.id)
        self.assertEqual(res.name, 'test network')
        new_name = 'test_network1'
        res = dbapi.networks_update(self.context, res.id,
                                    {'name': 'test_network1'})
        self.assertEqual(res.name, new_name)

    def test_networks_get_by_id_no_exist_raises(self):
        # Since no network is created, any id should raise
        self.assertRaises(exceptions.NotFound, dbapi.networks_get_by_id,
                          self.context, 4)

    def test_networks_delete(self):
        network = dbapi.networks_create(self.context, network1)
        # First make sure we have the network created
        res = dbapi.networks_get_by_id(self.context, network.id)
        self.assertEqual(res.id, network.id)
        # Delete the network
        dbapi.networks_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound, dbapi.networks_get_by_id,
                          self.context, res.id)


class NetworkDevicesDBTestCase(base.DBTestCase):

    def test_network_devices_create(self):
        try:
            dbapi.network_devices_create(self.context, device1)
        except Exception:
            self.fail("Network device create raised unexpected exception")

    def test_network_devices_get_all(self):
        dbapi.network_devices_create(self.context, device1)
        dbapi.network_devices_create(self.context, device2)
        filters = {}
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 2)

    def test_network_device_get_all_filter_region(self):
        dbapi.network_devices_create(self.context, device1)
        dbapi.network_devices_create(self.context, device2)
        filters = {
            'region_id': device1['region_id'],
        }
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['hostname'], 'switch1')

    def test_network_device_get_all_filter_name(self):
        dbapi.network_devices_create(self.context, device1)
        dbapi.network_devices_create(self.context, device2)

        name = device1['hostname']
        setup_res = dbapi.network_devices_get_all(self.context, {},
                                                  default_pagination)

        self.assertEqual(len(setup_res), 2)
        matches = [dev for dev in setup_res if dev['hostname'] == name]
        self.assertEqual(len(matches), 1)

        filters = {
            'name': name,
        }
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['hostname'], name)

    def test_network_device_get_all_filter_cell_id(self):
        region_id = 1
        cell1 = dbapi.cells_create(
            self.context,
            {
                'name': 'cell1',
                'project_id': project_id1,
                'region_id': region_id,
            }
        )
        cell2 = dbapi.cells_create(
            self.context,
            {
                'name': 'cell2',
                'project_id': project_id1,
                'region_id': region_id,
            }
        )
        dbapi.network_devices_create(
            self.context, dict(cell_id=cell1.id, **device1)
        )
        dbapi.network_devices_create(
            self.context, dict(cell_id=cell2.id, **device2)
        )

        setup_res = dbapi.network_devices_get_all(self.context, {},
                                                  default_pagination)

        self.assertEqual(len(setup_res), 2)
        matches = [dev for dev in setup_res if dev['cell_id'] == cell1.id]
        self.assertEqual(len(matches), 1)

        filters = {
            'cell_id': cell1.id,
        }
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['cell_id'], cell1.id)

    def test_network_device_get_all_filter_device_type(self):
        dbapi.network_devices_create(self.context, device1)
        dbapi.network_devices_create(self.context, device3)

        dev_type = device1['device_type']
        setup_res = dbapi.network_devices_get_all(self.context, {},
                                                  default_pagination)

        self.assertEqual(len(setup_res), 2)
        matches = [dev for dev in setup_res if dev['device_type'] == dev_type]
        self.assertEqual(len(matches), 1)

        filters = {
            'device_type': dev_type,
        }
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['device_type'], dev_type)

    def test_network_device_get_all_filter_id(self):
        dbapi.network_devices_create(self.context, device1)
        dbapi.network_devices_create(self.context, device2)

        setup_res = dbapi.network_devices_get_all(self.context, {},
                                                  default_pagination)

        self.assertEqual(len(setup_res), 2)

        dev_id = setup_res[0]['id']
        self.assertNotEqual(dev_id, setup_res[1]['id'])

        filters = {
            'id': dev_id
        }
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['id'], dev_id)

    def test_network_device_get_all_filter_ip_address(self):
        dbapi.network_devices_create(self.context, device1)
        dbapi.network_devices_create(self.context, device3)

        ip = device1['ip_address']
        setup_res = dbapi.network_devices_get_all(self.context, {},
                                                  default_pagination)

        self.assertEqual(len(setup_res), 2)
        matches = [dev for dev in setup_res if str(dev['ip_address']) == ip]
        self.assertEqual(len(matches), 1)

        filters = {
            'ip_address': ip,
        }
        res = dbapi.network_devices_get_all(self.context, filters,
                                            default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(str(res[0]['ip_address']), ip)

    def test_network_devices_get_by_id(self):
        device = dbapi.network_devices_create(self.context, device1)
        res = dbapi.network_devices_get_by_id(self.context, device.id)
        self.assertEqual(res.hostname, 'switch1')

    def test_network_devices_get_by_filter_no_exit(self):
        dbapi.network_devices_create(self.context, device1)
        filters = {"hostname": "foo"}
        res = dbapi.networks_get_all(self.context, filters,
                                     default_pagination)
        self.assertEqual(res, [])

    def test_network_devices_delete(self):
        device = dbapi.network_devices_create(self.context, device1)
        # First make sure we have the device
        res = dbapi.network_devices_get_by_id(self.context, device.id)
        self.assertEqual(res.id, device.id)
        # Delete the device
        dbapi.network_devices_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound, dbapi.network_devices_get_by_id,
                          self.context, res.id)

    def test_network_devices_labels_create(self):
        device = dbapi.network_devices_create(self.context, device1)
        labels = {"labels": ["tom", "jerry"]}
        dbapi.network_devices_labels_update(self.context, device.id, labels)

    def test_network_devices_update(self):
        device = dbapi.network_devices_create(self.context, device1)
        res = dbapi.network_devices_get_by_id(self.context, device.id)
        self.assertEqual(res.hostname, 'switch1')
        new_name = 'switch2'
        res = dbapi.network_devices_update(self.context, res.id,
                                           {'name': 'switch2'})
        self.assertEqual(res.name, new_name)

    def test_network_devices_labels_delete(self):
        device = dbapi.network_devices_create(self.context, device1)
        _labels = {"labels": ["tom", "jerry"]}
        dbapi.network_devices_labels_update(self.context, device.id, _labels)
        ndevice = dbapi.network_devices_get_by_id(self.context, device.id)
        self.assertEqual(sorted(ndevice.labels), sorted(_labels["labels"]))
        _dlabels = {"labels": ["tom"]}
        dbapi.network_devices_labels_delete(self.context, ndevice.id, _dlabels)
        ndevice = dbapi.network_devices_get_by_id(self.context, ndevice.id)
        self.assertEqual(ndevice.labels, {"jerry"})


class NetworkInterfacesDBTestCase(base.DBTestCase):

    def test_network_interfaces_create(self):
        try:
            dbapi.network_interfaces_create(self.context, network_interface1)
        except Exception:
            self.fail("Network interface create raised unexpected exception")

    def test_network_interfaces_get_all(self):
        dbapi.network_interfaces_create(self.context, network_interface1)
        dbapi.network_interfaces_create(self.context, network_interface2)
        filters = {}
        res = dbapi.network_interfaces_get_all(self.context, filters,
                                               default_pagination)
        self.assertEqual(len(res), 2)
        self.assertEqual(
            str(res[0]['ip_address']), network_interface1['ip_address']
        )
        self.assertEqual(
            str(res[1]['ip_address']), network_interface2['ip_address']
        )

    def test_interface_get_all_filter_device_id(self):
        dbapi.network_interfaces_create(self.context, network_interface1)
        dbapi.network_interfaces_create(self.context, network_interface2)
        filters = {
            "device_id": 1,
        }
        res = dbapi.network_interfaces_get_all(self.context, filters,
                                               default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'eth1')

    def test_network_interfaces_get_by_id(self):
        interface = dbapi.network_interfaces_create(self.context,
                                                    network_interface1)
        res = dbapi.network_interfaces_get_by_id(self.context, interface.id)
        self.assertEqual(res.name, 'eth1')
        self.assertEqual(str(res.ip_address), network_interface1['ip_address'])

    def test_network_interfaces_update(self):
        interface = dbapi.network_interfaces_create(self.context,
                                                    network_interface1)
        res = dbapi.network_interfaces_get_by_id(self.context, interface.id)
        self.assertEqual(res.name, 'eth1')
        new_name = 'eth2'
        res = dbapi.network_interfaces_update(self.context, interface.id,
                                              {'name': 'eth2'})
        self.assertEqual(res.name, new_name)
        self.assertEqual(str(res.ip_address), network_interface1['ip_address'])

    def test_network_interfaces_delete(self):
        interface = dbapi.network_interfaces_create(self.context,
                                                    network_interface1)
        # First make sure we have the interface created
        res = dbapi.network_interfaces_get_by_id(self.context, interface.id)
        self.assertEqual(res.id, interface.id)
        # Delete the device
        dbapi.network_interfaces_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound,
                          dbapi.network_interfaces_get_by_id,
                          self.context, res.id)
