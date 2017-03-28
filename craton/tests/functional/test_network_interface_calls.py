from craton.tests import functional


class APIv1NetworkInterfacesTest(functional.DeviceTestBase):
    def setUp(self):
        super(APIv1NetworkInterfacesTest, self).setUp()
        self.interfaces_url = self.url + '/v1/network-interfaces'

    def test_associate_network_device_with_a_host(self):
        host = self.create_host('host-0', 'server', '127.0.0.1')

        payload = {
            'name': 'lo',
            'ip_address': '127.0.0.1',
            'device_id': host['id'],
            'interface_type': 'loopback',
        }
        response = self.post(self.interfaces_url, data=payload)
        self.assertSuccessCreated(response)
        self.assertIn('Location', response.headers)
        interface = response.json()
        self.assertEqual(
            '{}/{}'.format(self.interfaces_url, interface['id']),
            response.headers['Location']
        )

    def test_port_must_be_an_integer_on_create(self):
        host = self.create_host('host-0', 'server', '127.0.0.1')

        payload = {
            'name': 'lo',
            'ip_address': '127.0.0.1',
            'device_id': host['id'],
            'interface_type': 'loopback',
            'port': 'asdf',
        }
        response = self.post(self.interfaces_url, data=payload)
        self.assertBadRequest(response)

    def test_port_must_be_an_integer_on_update(self):
        host = self.create_host('host-0', 'server', '127.0.0.1')

        payload = {
            'name': 'lo',
            'ip_address': '127.0.0.1',
            'device_id': host['id'],
            'interface_type': 'loopback',
            'port': 80,
        }
        response = self.post(self.interfaces_url, data=payload)
        self.assertSuccessCreated(response)
        interface = response.json()

        url = self.interfaces_url + '/{}'.format(interface['id'])
        payload = {'port': 'asdf'}
        response = self.put(url, data=payload)
        self.assertBadRequest(response)

    def test_network_interface_create_missing_all_properties_fails(self):
        url = self.url + '/v1/network-interfaces'
        network_interface = self.post(url, data={})
        self.assertEqual(400, network_interface.status_code)
        msg = (
            "The request included the following errors:\n"
            "- 'device_id' is a required property\n"
            "- 'interface_type' is a required property\n"
            "- 'ip_address' is a required property\n"
            "- 'name' is a required property"
        )
        self.assertEqual(network_interface.json()['message'], msg)
