from craton.tests import functional


class APIv1NetworkInterfacesTest(functional.DeviceTestBase):
    def setUp(self):
        super(APIv1NetworkInterfacesTest, self).setUp()
        self.interfaces_url = self.url + '/v1/network_interfaces'

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
