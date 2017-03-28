from craton.tests.functional import DeviceTestBase


class APIV1NetworkDeviceTest(DeviceTestBase):

    resource = 'network-devices'

    def test_create_with_parent_id(self):
        parent = self.create_network_device(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.1',
        )
        child = self.create_network_device(
            name='test2',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.2',
            parent_id=parent['id'],
        )
        self.assertEqual(parent['id'], child['parent_id'])

    def test_update_with_parent_id(self):
        parent = self.create_network_device(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.1',
        )

        child = self.create_network_device(
            name='test2',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.2',
        )
        self.assertIsNone(child['parent_id'])

        url = '{}/v1/network-devices/{}'.format(self.url, child['id'])
        child_update_resp = self.put(
            url, data={'parent_id': parent['id']}
        )
        self.assertEqual(200, child_update_resp.status_code)
        child_update = child_update_resp.json()
        self.assertEqual(parent['id'], child_update['parent_id'])

    def test_update_with_parent_id_equal_id_fails(self):
        network_device = self.create_network_device(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.1',
        )

        url = '{}/v1/network-devices/{}'.format(self.url, network_device['id'])
        network_device_update_resp = self.put(
            url, data={'parent_id': network_device['id']}
        )
        self.assertEqual(400, network_device_update_resp.status_code)

    def test_update_with_parent_id_equal_descendant_id_fails(self):
        parent = self.create_network_device(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.1',
        )
        self.assertIsNone(parent['parent_id'])

        child = self.create_network_device(
            name='test2',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.2',
            parent_id=parent['id'],
        )
        self.assertEqual(parent['id'], child['parent_id'])

        grandchild = self.create_network_device(
            name='test3',
            cloud=self.cloud,
            region=self.region,
            device_type='switch',
            ip_address='192.168.1.3',
            parent_id=child['id'],
        )
        self.assertEqual(child['id'], grandchild['parent_id'])

        url = '{}/v1/network-devices/{}'.format(self.url, parent['id'])
        parent_update_resp = self.put(
            url, data={'parent_id': grandchild['id']}
        )
        self.assertEqual(400, parent_update_resp.status_code)

    def test_network_device_create_missing_all_properties_fails(self):
        url = self.url + '/v1/network-devices'
        network_device = self.post(url, data={})
        self.assertEqual(400, network_device.status_code)
        msg = (
            "The request included the following errors:\n"
            "- 'cloud_id' is a required property\n"
            "- 'device_type' is a required property\n"
            "- 'ip_address' is a required property\n"
            "- 'name' is a required property\n"
            "- 'region_id' is a required property"
        )
        self.assertEqual(network_device.json()['message'], msg)
