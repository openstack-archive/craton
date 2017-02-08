import urllib.parse

from craton.tests.functional import TestCase
from craton.tests.functional.test_variable_calls import \
    APIV1ResourceWithVariablesTestCase


class HostTests(TestCase):
    def setUp(self):
        super(HostTests, self).setUp()
        self.cloud = self.create_cloud()
        self.region = self.create_region()

    def create_cloud(self):
        url = self.url + '/v1/clouds'
        payload = {'name': 'cloud-1'}
        cloud = self.post(url, data=payload)
        self.assertEqual(201, cloud.status_code)
        self.assertIn('Location', cloud.headers)
        self.assertEqual(
            cloud.headers['Location'],
            "{}/{}".format(url, cloud.json()['id'])
        )
        return cloud.json()

    def create_region(self, region_name='region-1'):
        url = self.url + '/v1/regions'
        payload = {'name': region_name, 'cloud_id': self.cloud['id']}
        region = self.post(url, data=payload)
        self.assertEqual(201, region.status_code)
        self.assertIn('Location', region.headers)
        self.assertEqual(
            region.headers['Location'],
            "{}/{}".format(url, region.json()['id'])
        )
        return region.json()

    def create_host(self, name, hosttype, ip_address, region=None, cloud=None,
                    **variables):
        if region is None:
            region = self.region

        if cloud is None:
            cloud = self.cloud

        url = self.url + '/v1/hosts'
        payload = {'name': name, 'device_type': hosttype,
                   'ip_address': ip_address,
                   'region_id': region['id'],
                   'cloud_id': cloud['id']}
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


class APIV1HostTest(HostTests, APIV1ResourceWithVariablesTestCase):

    resource = 'hosts'

    def test_create_host_supports_vars_ops(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        self.assert_vars_get_expected(host['id'], {})
        self.assert_vars_can_be_set(host['id'])
        self.assert_vars_can_be_deleted(host['id'])

    def test_host_get_by_vars_filter(self):
        vars1 = {"a": "b", "host": "one"}
        self.create_host('host1', 'server', '192.168.1.1', **vars1)
        vars2 = {"a": "b"}
        self.create_host('host2', 'server', '192.168.1.2', **vars2)

        url = self.url + '/v1/hosts'
        resp = self.get(url, vars='a:b')
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(2, len(hosts))
        self.assertEqual({'192.168.1.1', '192.168.1.2'},
                         {host['ip_address'] for host in hosts})

        url = self.url + '/v1/hosts'
        resp = self.get(url, vars='host:one')
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual('192.168.1.1', hosts[0]['ip_address'])
        self.assert_vars_get_expected(hosts[0]['id'], vars1)

    def test_create_host(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        self.assertEqual('host1', host['name'])

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

    def test_host_get_by_ip_filter(self):
        self.create_host('host1', 'server', '192.168.1.1')
        self.create_host('host2', 'server', '192.168.1.2')
        url = self.url + '/v1/hosts?ip_address=192.168.1.1'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual('192.168.1.1', hosts[0]['ip_address'])

    def test_host_by_missing_filter(self):
        self.create_host('host1', 'server', '192.168.1.1')
        url = self.url + '/v1/hosts?ip_address=192.168.1.2'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, len(resp.json()['hosts']))

    def test_host_create_labels(self):
        res = self.create_host('host1', 'server', '192.168.1.1')
        url = self.url + '/v1/hosts/{}/labels'.format(res['id'])

        data = {"labels": ["compute"]}
        resp = self.put(url, data=data)
        self.assertEqual(200, resp.status_code)

        resp = self.get(url)
        self.assertEqual(data, resp.json())

    def test_host_by_label_filter_match_one(self):
        labels_route_mask = '/v1/hosts/{}/labels'
        host1 = self.create_host('host1', 'server', '192.168.1.1')
        host2 = self.create_host('host2', 'server', '192.168.1.2')
        host3 = self.create_host('host3', 'server', '192.168.1.3')

        # set labels on hosts
        data = {"labels": ["compute"]}
        for host in (host1, host2, host3):
            url = self.url + labels_route_mask.format(host['id'])
            resp = self.put(url, data=data)
            self.assertEqual(200, resp.status_code)

        # set one of them with extra labels
        data = {"labels": ["compute", "scheduler"]}
        url = self.url + labels_route_mask.format(host3['id'])
        resp = self.put(url, data=data)
        self.assertEqual(200, resp.status_code)

        # get hosts by its label
        url = self.url + '/v1/hosts?label=scheduler'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host3['id'], hosts[0]['id'])

    def test_host_by_label_filters_match_all(self):
        labels_route_mask = '/v1/hosts/{}/labels'
        host1 = self.create_host('host1', 'server', '192.168.1.1')
        host2 = self.create_host('host2', 'server', '192.168.1.2')
        host3 = self.create_host('host3', 'server', '192.168.1.3')

        # set labels on hosts
        data = {"labels": ["compute"]}
        for host in (host1, host2, host3):
            url = self.url + labels_route_mask.format(host['id'])
            resp = self.put(url, data=data)
            self.assertEqual(200, resp.status_code)

        # set one of them with extra labels
        data = {"labels": ["compute", "scheduler"]}
        url = self.url + labels_route_mask.format(host2['id'])
        resp = self.put(url, data=data)
        self.assertEqual(200, resp.status_code)

        # get hosts by its label
        url = self.url + '/v1/hosts?label=scheduler&label=compute'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host2['id'], hosts[0]['id'])

    def test_host_by_label_filters_match_one_common(self):
        labels_route_mask = '/v1/hosts/{}/labels'
        test_hosts = [
            self.create_host('host1', 'server', '192.168.1.1'),
            self.create_host('host2', 'server', '192.168.1.2'),
            self.create_host('host3', 'server', '192.168.1.3'),
        ]

        # set labels on hosts
        data = {"labels": ["compute"]}
        for host in test_hosts:
            url = self.url + labels_route_mask.format(host['id'])
            resp = self.put(url, data=data)
            self.assertEqual(200, resp.status_code)

        # set one of them with extra labels
        data = {"labels": ["compute", "scheduler"]}
        url = self.url + labels_route_mask.format(test_hosts[1]['id'])
        resp = self.put(url, data=data)
        self.assertEqual(200, resp.status_code)

        # get hosts by its label
        url = self.url + '/v1/hosts?label=compute'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(3, len(hosts))
        self.assertEqual(sorted([host['id'] for host in test_hosts]),
                         sorted([host['id'] for host in hosts]))

    def test_host_delete(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        url = self.url + '/v1/hosts/{}'.format(host['id'])
        resp = self.delete(url)
        self.assertEqual(204, resp.status_code)

        resp = self.get(url)
        self.assertEqual(404, resp.status_code)
        self.assertEqual({'status': 404, 'message': 'Not Found'},
                         resp.json())


class TestPagination(HostTests):

    def setUp(self):
        super(TestPagination, self).setUp()
        self.hosts = [
            self.create_host('host{}'.format(i), 'server',
                             '192.168.1.{}'.format(i + 1))
            for i in range(0, 61)
        ]

    def test_get_returns_a_default_list_of_thirty_hosts(self):
        response = self.get(self.url + '/v1/hosts')
        self.assertSuccessOk(response)
        hosts = response.json()
        self.assertIn('hosts', hosts)
        self.assertEqual(30, len(hosts['hosts']))
        self.assertListEqual([h['id'] for h in self.hosts[:30]],
                             [h['id'] for h in hosts['hosts']])

    def test_get_returns_correct_next_link(self):
        thirtieth_host = self.hosts[29]
        response = self.get(self.url + '/v1/hosts')
        self.assertSuccessOk(response)
        hosts = response.json()
        self.assertIn('links', hosts)
        for link_rel in hosts['links']:
            if link_rel['rel'] == 'next':
                break
        else:
            self.fail("No 'next' link was returned in response")

        parsed_next = urllib.parse.urlparse(link_rel['href'])
        self.assertIn('marker={}'.format(thirtieth_host['id']),
                      parsed_next.query)

    def test_get_returns_correct_prev_link(self):
        first_host = self.hosts[0]
        thirtieth_host = self.hosts[29]
        url = self.url + '/v1/hosts?marker={}'.format(thirtieth_host['id'])
        response = self.get(url)
        self.assertSuccessOk(response)
        hosts = response.json()
        self.assertIn('links', hosts)
        for link_rel in hosts['links']:
            if link_rel['rel'] == 'prev':
                break
        else:
            self.fail("No 'prev' link was returned in response")

        parsed_prev = urllib.parse.urlparse(link_rel['href'])
        self.assertIn('marker={}'.format(first_host['id']), parsed_prev.query)

    def test_get_all_for_region(self):
        region = self.create_region('region-2')
        self.create_host('host1', 'server', '192.168.1.1', region=region)
        self.create_host('host2', 'server', '192.168.1.2', region=region)
        url = self.url + '/v1/hosts?region_id={}'.format(region['id'])
        resp = self.get(url)
        self.assertSuccessOk(resp)
        hosts = resp.json()
        self.assertEqual(2, len(hosts['hosts']))

    def test_ascending_sort_by_name(self):
        response = self.get(self.url + '/v1/hosts',
                            sort_keys='name', sort_dir='asc')
        self.assertSuccessOk(response)
        hosts = response.json()['hosts']
        self.assertEqual(30, len(hosts))

    def test_ascending_sort_by_name_and_id(self):
        response = self.get(self.url + '/v1/hosts',
                            sort_keys='name,id', sort_dir='asc')
        self.assertSuccessOk(response)
        hosts = response.json()['hosts']
        self.assertEqual(30, len(hosts))

    def test_ascending_sort_by_name_and_id_space_separated(self):
        response = self.get(self.url + '/v1/hosts',
                            sort_keys='name id', sort_dir='asc')
        self.assertSuccessOk(response)
        hosts = response.json()['hosts']
        self.assertEqual(30, len(hosts))
