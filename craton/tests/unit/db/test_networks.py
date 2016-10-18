import uuid

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base


project_id1 = uuid.uuid4().hex
network1 = {"name": "test network",
            "cidr": "192.168.1.0/24",
            "gateway": "192.168.1.1",
            "netmask": "255.255.255.0",
            "region_id": 1,
            "project_id": project_id1}

device1 = {"hostname": "switch1",
           "model_name": "Model-X",
           "region_id": 1,
           "project_id": project_id1,
           "device_type": "switch",
           "ip_address": "192.168.1.1"}

net_interface1 = {"device_id": 1,
                  "project_id": project_id1,
                  "name": "eth1",
                  "ip_address": "192.168.0.2",
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
        filters = {}
        res = dbapi.networks_get_by_region(self.context,
                                           network1['region_id'],
                                           filters)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'test network')

    def test_networks_get_by_id(self):
        network = dbapi.networks_create(self.context, network1)
        res = dbapi.networks_get_by_id(self.context, network.id)
        self.assertEqual(res.name, 'test network')

    def test_networks_get_by_name_filter_no_exit(self):
        filters = {"id": 5}
        res = dbapi.networks_get_by_region(self.context,
                                           network1['region_id'],
                                           filters)
        self.assertEqual(res, [])

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

    def test_netdevices_create(self):
        try:
            dbapi.netdevices_create(self.context, device1)
        except Exception:
            self.fail("Network device create raised unexpected exception")

    def test_netdevice_get_all(self):
        dbapi.netdevices_create(self.context, device1)
        filters = {}
        res = dbapi.netdevices_get_by_region(self.context,
                                             device1['region_id'],
                                             filters)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['hostname'], 'switch1')

    def test_netdevices_get_by_id(self):
        device = dbapi.netdevices_create(self.context, device1)
        res = dbapi.netdevices_get_by_id(self.context, device.id)
        self.assertEqual(res.hostname, 'switch1')

    def test_netdevices_get_by_filter_no_exit(self):
        filters = {"id": 5}
        res = dbapi.networks_get_by_region(self.context,
                                           device1['region_id'],
                                           filters)
        self.assertEqual(res, [])

    def test_netdevices_delete(self):
        device = dbapi.netdevices_create(self.context, device1)
        # First make sure we have the device
        res = dbapi.netdevices_get_by_id(self.context, device.id)
        self.assertEqual(res.id, device.id)
        # Delete the device
        dbapi.netdevices_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound, dbapi.netdevices_get_by_id,
                          self.context, res.id)

    def test_netdevice_labels_create(self):
        device = dbapi.netdevices_create(self.context, device1)
        labels = {"labels": ["tom", "jerry"]}
        dbapi.netdevices_labels_update(self.context, device.id, labels)

    def test_netdevice_labels_delete(self):
        device = dbapi.netdevices_create(self.context, device1)
        _labels = {"labels": ["tom", "jerry"]}
        dbapi.netdevices_labels_update(self.context, device.id, _labels)
        ndevice = dbapi.netdevices_get_by_id(self.context, device.id)
        self.assertEqual(sorted(ndevice.labels), sorted(_labels["labels"]))
        _dlabels = {"labels": ["tom"]}
        dbapi.netdevices_labels_delete(self.context, ndevice.id, _dlabels)
        ndevice = dbapi.netdevices_get_by_id(self.context, ndevice.id)
        self.assertEqual(ndevice.labels, {"jerry"})


class NetworkInterfacesDBTestCase(base.DBTestCase):

    def test_interface_create(self):
        try:
            dbapi.net_interfaces_create(self.context, net_interface1)
        except Exception:
            self.fail("Network interface create raised unexpected exception")

    def test_interface_get_all(self):
        dbapi.net_interfaces_create(self.context, net_interface1)
        filters = {}
        res = dbapi.net_interfaces_get_by_device(self.context, 1, filters)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'eth1')

    def test_interface_get_by_id(self):
        interface = dbapi.net_interfaces_create(self.context, net_interface1)
        res = dbapi.net_interfaces_get_by_id(self.context, interface.id)
        self.assertEqual(res.name, 'eth1')

    def test_interface_delete(self):
        interface = dbapi.net_interfaces_create(self.context, net_interface1)
        # First make sure we have the interface created
        res = dbapi.net_interfaces_get_by_id(self.context, interface.id)
        self.assertEqual(res.id, interface.id)
        # Delete the device
        dbapi.net_interfaces_delete(self.context, res.id)
        self.assertRaises(exceptions.NotFound, dbapi.net_interfaces_get_by_id,
                          self.context, res.id)
