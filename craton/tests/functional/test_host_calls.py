import urllib.parse

from craton.tests.functional import DeviceTestBase
from craton.tests.functional.test_variable_calls import \
    APIV1ResourceWithVariablesTestCase


class APIV1HostTest(DeviceTestBase, APIV1ResourceWithVariablesTestCase):

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

    def test_create_with_extra_id_property_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'device_type': 'server', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id'],
                   'cloud_id': self.cloud['id'], 'name': 'a', 'id': 1}
        host = self.post(url, data=payload)
        self.assertEqual(400, host.status_code)
        msg = (
            "The request included the following errors:\n"
            "- Additional properties are not allowed ('id' was unexpected)"
        )
        self.assertEqual(host.json()['message'], msg)

    def test_create_with_extra_created_at_property_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'device_type': 'server', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id'],
                   'cloud_id': self.cloud['id'], 'name': 'a',
                   'created_at': 'some date'}
        host = self.post(url, data=payload)
        self.assertEqual(400, host.status_code)
        msg = (
            "The request included the following errors:\n"
            "- Additional properties are not allowed "
            "('created_at' was unexpected)"
        )
        self.assertEqual(host.json()['message'], msg)

    def test_create_with_extra_updated_at_property_fails(self):
        url = self.url + '/v1/hosts'
        payload = {'device_type': 'server', 'ip_address': '192.168.1.1',
                   'region_id': self.region['id'],
                   'cloud_id': self.cloud['id'], 'name': 'a',
                   'updated_at': 'some date'}
        host = self.post(url, data=payload)
        self.assertEqual(400, host.status_code)
        msg = (
            "The request included the following errors:\n"
            "- Additional properties are not allowed "
            "('updated_at' was unexpected)"
        )
        self.assertEqual(host.json()['message'], msg)

    def test_create_missing_all_properties_fails(self):
        url = self.url + '/v1/hosts'
        host = self.post(url, data={})
        self.assertEqual(400, host.status_code)
        msg = (
            "The request included the following errors:\n"
            "- 'cloud_id' is a required property\n"
            "- 'device_type' is a required property\n"
            "- 'ip_address' is a required property\n"
            "- 'name' is a required property\n"
            "- 'region_id' is a required property"
        )
        self.assertEqual(host.json()['message'], msg)

    def test_create_with_parent_id(self):
        parent = self.create_host(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.1',
        )
        child = self.create_host(
            name='test2',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.2',
            parent_id=parent['id'],
        )
        self.assertEqual(parent['id'], child['parent_id'])

    def test_update_with_parent_id(self):
        parent = self.create_host(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.1',
        )

        child = self.create_host(
            name='test2',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.2',
        )
        self.assertIsNone(child['parent_id'])

        url = '{}/v1/hosts/{}'.format(self.url, child['id'])
        child_update_resp = self.put(
            url, data={'parent_id': parent['id']}
        )
        self.assertEqual(200, child_update_resp.status_code)
        child_update = child_update_resp.json()
        self.assertEqual(parent['id'], child_update['parent_id'])

    def test_update_with_parent_id_equal_id_fails(self):
        host = self.create_host(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.1',
        )

        url = '{}/v1/hosts/{}'.format(self.url, host['id'])
        host_update_resp = self.put(
            url, data={'parent_id': host['id']}
        )
        self.assertEqual(400, host_update_resp.status_code)

    def test_update_with_parent_id_equal_descendant_id_fails(self):
        parent = self.create_host(
            name='test1',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.1',
        )
        self.assertIsNone(parent['parent_id'])

        child = self.create_host(
            name='test2',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.2',
            parent_id=parent['id'],
        )
        self.assertEqual(parent['id'], child['parent_id'])

        grandchild = self.create_host(
            name='test3',
            cloud=self.cloud,
            region=self.region,
            hosttype='server',
            ip_address='192.168.1.3',
            parent_id=child['id'],
        )
        self.assertEqual(child['id'], grandchild['parent_id'])

        url = '{}/v1/hosts/{}'.format(self.url, parent['id'])
        parent_update_resp = self.put(
            url, data={'parent_id': grandchild['id']}
        )
        self.assertEqual(400, parent_update_resp.status_code)

    def test_get_all_hosts_with_details(self):
        region_vars = {'x': 'y'}
        region = self.create_region(name='region1', variables=region_vars)
        variables = {"a": "b"}
        self.create_host('host1', 'server', '192.168.1.1', region=region,
                         **variables)
        self.create_host('host2', 'server', '192.168.1.2', region=region,
                         **variables)
        url = self.url + '/v1/hosts?details=all'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        hosts = resp.json()['hosts']
        self.assertEqual(2, len(hosts))
        for host in hosts:
            self.assertTrue('variables' in host)
            self.assertEqual({'a': 'b', 'x': 'y'}, host['variables'])

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

    def test_host_get_all_vars_filter_resolved_region(self):
        region_vars = {'foo': 'bar'}
        region = self.create_region(name='region-2', variables=region_vars)
        host_vars = {'baz': 'zoo'}
        self.create_host('host1', 'server', '192.168.1.1', **host_vars)
        host2 = self.create_host('host2', 'server', '192.168.1.2',
                                 region=region, **host_vars)
        url = self.url + '/v1/hosts'

        resp = self.get(url, vars="foo:bar,baz:zoo")
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host2['id'], hosts[0]['id'])

    def test_host_get_all_vars_filter_resolved_region_and_host(self):
        region_vars = {'foo': 'bar'}
        region = self.create_region(name='region-2', variables=region_vars)
        host_vars = {'baz': 'zoo'}
        host1 = self.create_host('host1', 'server', '192.168.1.1',
                                 **region_vars)
        host2 = self.create_host('host2', 'server', '192.168.1.2',
                                 region=region, **host_vars)
        url = self.url + '/v1/hosts'

        resp = self.get(url, vars='foo:bar')
        hosts = resp.json()['hosts']
        self.assertEqual(2, len(hosts))
        self.assertListEqual(sorted([host1['id'], host2['id']]),
                             sorted([host['id'] for host in hosts]))

    def test_host_get_all_vars_filter_resolved_region_child_override(self):
        region_vars = {'foo': 'bar'}
        region = self.create_region(name='region-2', variables=region_vars)
        host1 = self.create_host('host1', 'server', '192.168.1.1',
                                 region=region, foo='baz')
        host2 = self.create_host('host2', 'server', '192.168.1.2',
                                 region=region)
        url = self.url + '/v1/hosts'

        resp = self.get(url, vars='foo:baz')
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host1['id'], hosts[0]['id'])

        resp = self.get(url, vars='foo:bar')
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host2['id'], hosts[0]['id'])

    def test_host_get_all_vars_filter_resolved_host_child_override(self):
        host1 = self.create_host('host1', 'server', '192.168.1.1',
                                 baz='zoo')
        host2 = self.create_host('host2', 'server', '192.168.1.2',
                                 parent_id=host1['id'], baz='boo')
        url = self.url + '/v1/hosts'

        resp = self.get(url, vars='baz:zoo')
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host1['id'], hosts[0]['id'])

        resp = self.get(url, vars='baz:boo')
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host2['id'], hosts[0]['id'])

    def test_host_get_all_vars_filter_unresolved(self):
        host1 = self.create_host('host1', 'server', '192.168.1.1',
                                 foo='bar', baz='zoo')
        self.create_host('host2', 'server', '192.168.1.2', foo='bar')

        # NOTE(thomasem): Unfortunately, we use resolved-values instead of
        # resolved_values, so we can't pass this in as kwargs to self.get(...),
        # see https://bugs.launchpad.net/craton/+bug/1672880.
        url = self.url + '/v1/hosts?resolved-values=false&vars=foo:bar,baz:zoo'

        resp = self.get(url)
        hosts = resp.json()['hosts']
        self.assertEqual(1, len(hosts))
        self.assertEqual(host1['id'], hosts[0]['id'])

    def test_host_delete(self):
        host = self.create_host('host1', 'server', '192.168.1.1')
        url = self.url + '/v1/hosts/{}'.format(host['id'])
        resp = self.delete(url)
        self.assertEqual(204, resp.status_code)

        resp = self.get(url)
        self.assertEqual(404, resp.status_code)
        self.assertEqual({'status': 404, 'message': 'Not Found'},
                         resp.json())


class TestPagination(DeviceTestBase):

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

    def test_get_all_for_cloud(self):
        cloud = self.create_cloud('cloud-2')
        region = self.create_region(cloud=cloud)
        self.create_host('host1', 'server', '192.168.1.1', cloud=cloud,
                         region=region)
        self.create_host('host2', 'server', '192.168.1.2', cloud=cloud,
                         region=region)
        url = self.url + '/v1/hosts?cloud_id={}'.format(cloud['id'])
        resp = self.get(url)
        self.assertSuccessOk(resp)
        hosts = resp.json()['hosts']
        self.assertEqual(2, len(hosts))
        self.assertEqual(['host1', 'host2'], [h['name'] for h in hosts])

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

    def test_follows_next_link(self):
        url = self.url + '/v1/hosts'
        response = self.get(url)
        self.assertSuccessOk(response)
        json = response.json()
        hosts = json['hosts']
        while hosts:
            for link in json['links']:
                if link['rel'] == 'next':
                    break
            else:
                break
            response = self.get(link['href'])
            self.assertSuccessOk(response)
            json = response.json()
            hosts = json['hosts']
