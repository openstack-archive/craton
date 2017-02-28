from craton.tests.functional import TestCase


class APIV1NetworkSchemaTest(TestCase):

    def setUp(self):
        super(APIV1NetworkSchemaTest, self).setUp()
        self.cloud = self.create_cloud(name='cloud-1')
        self.region = self.create_region(name='region-1', cloud=self.cloud)
        self.networks_url = self.url + '/v1/networks'
        self.cidr = '192.168.0.0/24'
        self.netmask = '255.255.255.0'
        self.gateway = '192.168.0.1'

    def test_network_create_with_required_works(self):
        payload = {
            'cloud_id': self.cloud['id'],
            'region_id': self.region['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
        }
        resp = self.post(self.networks_url, data=payload)
        self.assertEqual(201, resp.status_code)

        network = resp.json()
        self.assertEqual('a', network['name'])
        self.assertEqual(self.cloud['id'], network['cloud_id'])
        self.assertEqual(self.region['id'], network['region_id'])
        self.assertEqual(self.cidr, network['cidr'])
        self.assertEqual(self.gateway, network['gateway'])
        self.assertEqual(self.netmask, network['netmask'])

    def test_network_create_without_region_id_fails(self):
        payload = {
            'cloud_id': self.cloud['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
        }
        network = self.post(self.networks_url, data=payload)
        self.assertEqual(400, network.status_code)
        msg = ["'region_id' is a required property"]
        self.assertEqual(network.json()['errors'], msg)

    def test_network_create_without_cloud_id_fails(self):
        payload = {
            'region_id': self.region['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
        }
        network = self.post(self.networks_url, data=payload)
        self.assertEqual(400, network.status_code)
        msg = ["'cloud_id' is a required property"]
        self.assertEqual(network.json()['errors'], msg)

    def test_network_create_with_extra_id_property_fails(self):
        payload = {
            'region_id': self.region['id'],
            'cloud_id': self.cloud['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'id': 3
        }
        network = self.post(self.networks_url, data=payload)
        self.assertEqual(400, network.status_code)
        msg = ["Additional properties are not allowed ('id' was unexpected)"]
        self.assertEqual(network.json()['errors'], msg)

    def test_network_create_with_extra_created_at_property_fails(self):
        payload = {
            'region_id': self.region['id'],
            'cloud_id': self.cloud['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'created_at': 'This should not work'
        }
        network = self.post(self.networks_url, data=payload)
        self.assertEqual(400, network.status_code)
        msg = ["Additional properties are not allowed ('created_at' was "
               "unexpected)"]
        self.assertEqual(network.json()['errors'], msg)

    def test_network_create_with_extra_updated_at_property_fails(self):
        payload = {
            'region_id': self.region['id'],
            'cloud_id': self.cloud['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'updated_at': 'This should not work'
        }
        network = self.post(self.networks_url, data=payload)
        self.assertEqual(400, network.status_code)
        msg = ["Additional properties are not allowed ('updated_at' was "
               "unexpected)"]
        self.assertEqual(network.json()['errors'], msg)

    def test_network_get_all_with_details(self):
        payload = {
            'cloud_id': self.cloud['id'],
            'region_id': self.region['id'],
            'name': 'a',
            'cidr': self.cidr,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'variables': {'a': 'b'},
        }
        resp = self.post(self.networks_url, data=payload)
        self.assertEqual(201, resp.status_code)

        payload['name'] = 'b'
        resp = self.post(self.networks_url, data=payload)
        self.assertEqual(201, resp.status_code)

        url = self.networks_url + '?details=all'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        networks = resp.json()['networks']

        for network in networks:
            self.assertTrue('variables' in network)
            self.assertEqual({'a':'b'}, network['variables'])
