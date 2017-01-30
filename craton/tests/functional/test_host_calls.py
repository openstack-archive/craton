from craton.tests.functional import TestCase


class APIV1HostTest(TestCase):

    def setUp(self):
        super(APIV1HostTest, self).setUp()
        self.region = self.create_region()

    def tearDown(self):
        super(APIV1HostTest, self).tearDown()

    def create_region(self):
        url = self.url + '/v1/regions'
        payload = {'name': 'region-1'}
        region = self.post(url, data=payload)
        self.assertEqual(200, region.status_code)
        return region.json()

    def create_host(self, name, hosttype, ip_address, **variables):
        url = self.url + '/v1/hosts'
        payload = {'name': name, 'device_type': hosttype,
                   'ip_address': ip_address,
                   'region_id': self.region['id']}
        if variables:
            payload['variables'] = variables

        host = self.post(url, data=payload)
        self.assertEqual(200, host.status_code)
        return host.json()

    def test_create_host(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        self.assertEqual('host1', host['name'])

    def test_create_with_missing_name_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'device_type': 'server', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id']}
        host = self.post(url, data=payload)
        self.assertEqual(422, host.status_code)

    def test_create_with_missing_ip_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'name': 'test', 'device_type': 'server',
                   'region_id': self.region['id']}
        host = self.post(url, data=payload)
        self.assertEqual(422, host.status_code)

    def test_create_with_missing_type_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'name': 'who', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id']}
        host = self.post(url, data=payload)
        self.assertEqual(422, host.status_code)

    def test_host_get_all_for_region(self):
        self.create_host('host1', 'server', '192.168.1.1')
        self.create_host('host2', 'server', '192.168.1.2')
        url = self.url + '/v1/hosts?region_id={}'.format(self.region['id'])
        resp = self.get(url)
        self.assertEqual(2, len(resp.json()))

    def test_host_get_by_ip_filter(self):
        self.create_host('host1', 'server', '192.168.1.1')
        self.create_host('host2', 'server', '192.168.1.2')
        url = self.url + '/v1/hosts?ip_address=192.168.1.1'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, len(resp.json()))

    def test_host_by_missing_filter(self):
        self.create_host('host1', 'server', '192.168.1.1')
        url = self.url + '/v1/hosts?ip_address=192.168.1.2'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, len(resp.json()))

    def test_host_delete(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        url = self.url + '/v1/hosts/{}'.format(host['id'])
        resp = self.delete(url)
        self.assertEqual(204, resp.status_code)

        resp = self.get(url)
        self.assertEqual(404, resp.status_code)
        self.assertEqual({'status': 404, 'message': 'Not Found'},
                         resp.json())
