from craton.tests import functional


TEST_ARRAY = [
    1,
    23.4,
    True,
    False,
    'false',
    "I'm just a string",
    {
        'bumbleywump': 'cucumberpatch',
        'literal_boolean': 'true'
    },
    ['sub', 'array', True]
]

TEST_DICT = {
    'foo': {
        'nested_string': 'Bumbleywump Cucumberpatch',
        'nested_bool': True,
        'nested_null': None,
        'nested_int': 1,
        'nested_float': 3.14,
        'nested_boolstr': 'false',
        'hyphenated-key': 'look-at-all-these-hyphens!',
    },
    'bar': TEST_ARRAY,
    'baz': 'zoo'
}


class JSONPathSearchTestCaseMixin(object):

    resource = '<resource>'

    def get_resource_url(self):
        return '{}/v1/{}'.format(self.url, self.resource)

    def setup_projects(self, projects):
        created = []
        for name, variables in projects:
            created.append(self.create_project(
                name=name,
                variables=variables
            ))
        return created

    def setup_clouds(self, clouds):
        created = []
        for name, variables in clouds:
            created.append(self.create_cloud(
                name=name,
                variables=variables
            ))
        return created

    def setup_regions(self, regions):
        created = []
        cloud = self.create_cloud(name='cloud1')
        for name, variables in regions:
            created.append(self.create_region(
                name=name,
                cloud=cloud,
                variables=variables
            ))
        return created

    def setup_cells(self, cells):
        created = []
        cloud = self.create_cloud(name='cloud1')
        region = self.create_region(
            name='region1',
            cloud=cloud
        )
        for name, variables in cells:
            created.append(self.create_cell(
                name=name,
                cloud=cloud,
                region=region,
                variables=variables
            ))
        return created

    def setup_networks(self, networks):
        created = []
        cloud = self.create_cloud(name='cloud1')
        region = self.create_region(
            name='region1',
            cloud=cloud
        )
        for name, variables in networks:
            created.append(self.create_network(
                name=name,
                cloud=cloud,
                region=region,
                cidr='192.168.0.0/24',
                gateway='192.168.0.1',
                netmask='255.255.255.0',
                variables=variables
            ))
        return created

    def setup_network_devices(self, network_devices):
        created = []
        cloud = self.create_cloud(name='cloud1')
        region = self.create_region(
            name='region1',
            cloud=cloud
        )
        for name, variables in network_devices:
            created.append(self.create_network_device(
                name=name,
                cloud=cloud,
                region=region,
                device_type='switch',
                ip_address='192.168.0.1',
                **variables
            ))
        return created

    def setup_hosts(self, hosts):
        created = []
        cloud = self.create_cloud(name='cloud1')
        region = self.create_region(
            name='region1',
            cloud=cloud
        )
        for name, variables in hosts:
            created.append(self.create_host(
                name=name,
                cloud=cloud,
                region=region,
                hosttype='server',
                ip_address='192.168.0.1',
                **variables
            ))
        return created

    def setup_resources(self, resources):
        setup_fn = {
            "projects": self.setup_projects,
            "clouds": self.setup_clouds,
            "regions": self.setup_regions,
            "cells": self.setup_cells,
            "networks": self.setup_networks,
            "network-devices": self.setup_network_devices,
            "hosts": self.setup_hosts,
        }
        return setup_fn[self.resource](resources)

    def get_resources(self, **params):
        headers = None
        if self.resource in ('projects',):
            headers = self.root_headers
        resp = self.get(self.get_resource_url(), headers=headers,
                        details='all', **params)
        return resp.json()[self.resource.replace('-', '_')]

    def test_jsonpath_search_nested_string(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {'baz': 'nope'}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(
            vars='foo.foo.nested_string:"Bumbleywump Cucumberpatch"')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])

    def test_jsonpath_search_nested_string_wildcard(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"baz": "zoom"}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.*:"zoo"')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])

    def test_jsonpath_search_array_string(self):
        resources = (
            ('resource1', {'foo': TEST_ARRAY}),
            ('resource2', {'foo': TEST_ARRAY}),
            ('resource3', {'foo': ["I'm just a string", 1, 2, 3, 4, 'foo']}),
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo[5]:"I\'m just a string"')

        self.assertEqual(2, len(found))
        self.assertListEqual(sorted([c['id'] for c in created[:2]]),
                             sorted([f['id'] for f in found]))

    def test_jsonpath_search_array_string_wildcard(self):
        resources = (
            ('resource1', {'foo': TEST_ARRAY}),
            ('resource2', {'foo': TEST_ARRAY}),
            ('resource3', {'foo': ["I'm just a string", True]}),
            ('resource4', {'foo': ['Bumbleywump Cucumberpatch']}),
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo[*]:"I\'m just a string"')

        self.assertEqual(3, len(found))
        self.assertListEqual(sorted([c['id'] for c in created[:3]]),
                             sorted([f['id'] for f in found]))

    def test_jsonpath_search_nested_array_string(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': TEST_DICT}),
            ('resource3', {'foo': {"bar": ["I'm just a string", True]}}),
            ('resource4', {'foo': TEST_ARRAY}),
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.bar[*]:"I\'m just a string"')

        self.assertEqual(3, len(found))
        self.assertListEqual(sorted([c['id'] for c in created[:3]]),
                             sorted([f['id'] for f in found]))

    def test_jsonpath_search_nested_int(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"foo": {"nested_int": "1"}}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.foo.nested_int:1')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])

    def test_jsonpath_search_nested_float(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"foo": {"nested_float": 3}}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.foo.nested_float:3.14')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])

    def test_jsonpath_search_nested_bool(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"foo": {"nested_bool": 'true'}}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.foo.nested_bool:true')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])

    def test_jsonpath_search_nested_boolstr(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"foo": {"nested_boolstr": False}}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.foo.nested_boolstr:"false"')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])

    def test_jsonpath_search_nested_null(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"foo": {"nested_null": 'test'}}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.foo.nested_null:null')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])


    def test_jsonpath_search_hyphenated(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': {"foo": {"hyphenated-key": 'test-test'}}})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(
            vars='foo.foo."hyphenated-key":"look-at-all-these-hyphens"')

        self.assertEqual(1, len(found))
        self.assertEqual(created[0]['id'], found[0]['id'])
        self.assertEqual(created[0]['variables'], found[0]['variables'])


class ProjectsJSONPathSearchTestCase(functional.TestCase,
                                     JSONPathSearchTestCaseMixin):
    resource = 'projects'


class CloudsJSONPathSearchTestCase(functional.TestCase,
                                   JSONPathSearchTestCaseMixin):
    resource = 'clouds'


class RegionsJSONPathSearchTestCase(functional.TestCase,
                                    JSONPathSearchTestCaseMixin):
    resource = 'regions'


class CellsJSONPathSearchTestCase(functional.TestCase,
                                  JSONPathSearchTestCaseMixin):
    resource = 'cells'


class NetworksJSONPathSearchTestCase(functional.TestCase,
                                     JSONPathSearchTestCaseMixin):
    resource = 'networks'


class NetworkDevicesJSONPathSearchTestCase(functional.TestCase,
                                           JSONPathSearchTestCaseMixin):
    resource = 'network-devices'


class HostsJSONPathSearchTestCase(functional.TestCase,
                                  JSONPathSearchTestCaseMixin):
    resource = 'hosts'
