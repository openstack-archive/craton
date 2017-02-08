from itertools import count, cycle
import urllib.parse

from craton.tests.functional import DeviceTestBase


class DeviceTests(DeviceTestBase):

    def count_devices(self, devices):
        num_devices = (
            len(devices['hosts']) +
            len(devices['network-devices'])
        )
        return num_devices


class APIV1DeviceTest(DeviceTests):

    def setUp(self):
        super().setUp()
        self.net_device1 = self.create_network_device(
            'network_device1', 'switch', '192.168.1.1'
        )
        self.net_device2 = self.create_network_device(
            'network_device2', 'switch', '192.168.1.2',
            parent_id=self.net_device1['id'],
        )
        self.host1 = self.create_host(
            'host1', 'server', '192.168.1.3', parent_id=self.net_device2['id']
        )
        self.container1 = self.create_host(
            'host1container1', 'container', '192.168.1.4',
            parent_id=self.host1['id'],
        )
        url = self.url + '/v1/devices'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        devices = resp.json()['devices']
        self.assertEqual(4, self.count_devices(devices))

    def test_device_get_by_parent_id_no_descendants(self):
        url = '{}/v1/devices?parent_id={}'.format(
            self.url, self.net_device1['id']
        )
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        devices = resp.json()['devices']
        self.assertEqual(1, self.count_devices(devices))
        self.assertEqual(
            self.net_device1['id'], devices['network-devices'][0]['parent_id']
        )

    def test_device_get_by_parent_id_with_descendants(self):
        url = '{}/v1/devices?parent_id={}&descendants=true'.format(
            self.url, self.net_device1['id']
        )
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        devices = resp.json()['devices']
        self.assertEqual(3, self.count_devices(devices))
        self.assertEqual(
            self.net_device1['id'], devices['network-devices'][0]['parent_id']
        )
        self.assertEqual(
            self.net_device2['id'], devices['hosts'][0]['parent_id']
        )
        self.assertEqual(self.host1['id'], devices['hosts'][1]['parent_id'])

    def test_device_by_missing_filter(self):
        url = self.url + '/v1/devices?active=false'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        devices = resp.json()['devices']
        self.assertEqual(0, self.count_devices(devices))


class TestPagination(DeviceTests):

    def setUp(self):
        super().setUp()
        self.devices = []
        last_octet = count(1)

        first_network_device = self.create_network_device(
            'network-device0',
            'switch',
            '192.168.1.{}'.format(next(last_octet)),
        )
        self.devices.append(first_network_device)

        for i in range(1, 3):
            network_device = self.create_network_device(
                'network-device{}'.format(i),
                'switch',
                '192.168.1.{}'.format(next(last_octet)),
            )
            self.devices.append(network_device)
        host_parents = (
            self.devices[1],
            self.devices[2],
        )
        for i, host_parent in zip(range(12), cycle(host_parents)):
            host = self.create_host(
                'host{}'.format(i),
                'server',
                '192.168.1.{}'.format(next(last_octet)),
                parent_id=host_parent['id'],
            )
            self.devices.append(host)

            for j in range(4):
                container = self.create_host(
                    'host{}container{}'.format(i, j),
                    'container',
                    '192.168.1.{}'.format(next(last_octet)),
                    parent_id=host['id'],
                )
                self.devices.append(container)

    def test_get_returns_a_default_list_of_thirty_devices(self):
        response = self.get(self.url + '/v1/devices')
        self.assertSuccessOk(response)
        devices = response.json()
        self.assertIn('devices', devices)
        self.assertEqual(30, self.count_devices(devices['devices']))
        returned_device_ids = sorted(
            device['id']
            for dt in devices['devices'].values()
            for device in dt
        )
        self.assertListEqual(
            [d['id'] for d in self.devices[:30]],
            returned_device_ids
        )

    def test_get_returns_correct_next_link(self):
        thirtieth_device = self.devices[29]
        response = self.get(self.url + '/v1/devices')
        self.assertSuccessOk(response)
        devices = response.json()
        self.assertIn('links', devices)
        for link_rel in devices['links']:
            if link_rel['rel'] == 'next':
                break
        else:
            self.fail("No 'next' link was returned in response")

        parsed_next = urllib.parse.urlparse(link_rel['href'])
        self.assertIn('marker={}'.format(thirtieth_device['id']),
                      parsed_next.query)

    def test_get_returns_correct_prev_link(self):
        first_device = self.devices[0]
        thirtieth_device = self.devices[29]
        url = self.url + '/v1/devices?marker={}'.format(thirtieth_device['id'])
        response = self.get(url)
        self.assertSuccessOk(response)
        devices = response.json()
        self.assertIn('links', devices)
        for link_rel in devices['links']:
            if link_rel['rel'] == 'prev':
                break
        else:
            self.fail("No 'prev' link was returned in response")

        parsed_prev = urllib.parse.urlparse(link_rel['href'])
        self.assertIn(
            'marker={}'.format(first_device['id']), parsed_prev.query
        )

    def test_ascending_sort_by_name(self):
        response = self.get(self.url + '/v1/devices',
                            sort_keys='name', sort_dir='asc')
        self.assertSuccessOk(response)
        devices = response.json()['devices']
        self.assertEqual(30, self.count_devices(devices))

    def test_ascending_sort_by_name_and_id(self):
        response = self.get(self.url + '/v1/devices',
                            sort_keys='name,id', sort_dir='asc')
        self.assertSuccessOk(response)
        devices = response.json()['devices']
        self.assertEqual(30, self.count_devices(devices))

    def test_ascending_sort_by_name_and_id_space_separated(self):
        response = self.get(self.url + '/v1/devices',
                            sort_keys='name id', sort_dir='asc')
        self.assertSuccessOk(response)
        devices = response.json()['devices']
        self.assertEqual(30, self.count_devices(devices))
