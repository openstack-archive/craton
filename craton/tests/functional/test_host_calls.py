from craton.tests.functional.test_variable_calls import \
    APIV1ResourceWithVariablesTestCase


class APIV1HostTest(APIV1ResourceWithVariablesTestCase):

    resource = 'hosts'

    def setUp(self):
        super(APIV1HostTest, self).setUp()
        self.region = self.create_region()

    def tearDown(self):
        super(APIV1HostTest, self).tearDown()

    def create_region(self):
        url = self.url + '/v1/regions'
        payload = {'name': 'region-1'}
        region = self.post(url, data=payload)
        self.assertEqual(201, region.status_code)
        self.assertIn('Location', region.headers)
        self.assertEqual(
            region.headers['Location'],
            "{}/{}".format(url, region.json()['id'])
        )
        return region.json()

    def create_host(self, name, hosttype, ip_address, **variables):
        url = self.url + '/v1/hosts'
        payload = {'name': name, 'device_type': hosttype,
                   'ip_address': ip_address,
                   'region_id': self.region['id']}
        if variables:
            payload['variables'] = variables

        host = self.post(url, data=payload)
        self.assertEqual(201, host.status_code)
        self.assertIn('Location', host.headers)
        self.assertEqual(
            host.headers['Location'],
            "{}/{}".format(url, host.json()['id'])
        )
        return host.json()

    def test_create_host(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        self.assertEqual('host1', host['name'])
        self.assert_vars_get_expected(host['id'], {})
        self.assert_vars_can_be_set(host['id'])
        self.assert_vars_can_be_deleted(host['id'])

    def test_create_with_missing_name_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'device_type': 'server', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id']}
        host = self.post(url, data=payload)
        self.assertEqual(400, host.status_code)

    def test_create_with_missing_ip_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'name': 'test', 'device_type': 'server',
                   'region_id': self.region['id']}
        host = self.post(url, data=payload)
        self.assertEqual(400, host.status_code)

    def test_create_with_missing_type_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'name': 'who', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id']}
        host = self.post(url, data=payload)
        self.assertEqual(400, host.status_code)

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
        hosts = resp.json()
        self.assertEqual(1, len(hosts))
        self.assertEqual('192.168.1.1', hosts[0]['ip_address'])

    def test_host_get_by_vars_filter(self):
        vars1 = {"a": "b", "host": "one"}
        self.create_host('host1', 'server', '192.168.1.1', **vars1)
        vars2 = {"a": "b"}
        self.create_host('host2', 'server', '192.168.1.2', **vars2)

        url = self.url + '/v1/hosts?vars=a:b'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()
        self.assertEqual(2, len(hosts))
        self.assertEqual({'192.168.1.1', '192.168.1.2'},
                         {host['ip_address'] for host in hosts})

        url = self.url + '/v1/hosts?vars=host:one'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()
        self.assertEqual(1, len(hosts))
        self.assertEqual('192.168.1.1', hosts[0]['ip_address'])
        self.assert_vars_get_expected(hosts[0]['id'], vars1)

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
