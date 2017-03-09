from craton.tests import functional


TEST_ARRAY = [
    1,
    23.4,
    True,
    False,
    '"false"',
    {
        'bumbleywump': 'cucumberpatch',
        'literal_boolean': '"true"'
    },
    ['sub', 'array', True]
]

TEST_DICT = {
    'foo': {
        'bar': TEST_ARRAY
    },
    'baz': 'zoo'
}

TEST_STRING = 'bar'


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

    def setup_resources(self, resources):
        setup_fn = {
            "projects": self.setup_projects,
            "clouds": self.setup_clouds,
            "regions": self.setup_regions,
            "cells": self.setup_cells,
            "networks": self.setup_networks,
            # "network-devices": self.setup_network_devices,
            # "hosts": self.setup_hosts,
        }
        return setup_fn[self.resource](resources)

    def get_resources(self, **params):
        headers = None
        if self.resource in ('projects',):
            headers = self.root_headers
        resp = self.get(self.get_resource_url(), headers=headers,
                        details='all', **params)
        print("TEM resp.json(): %s" % str(resp.json()))
        return resp.json()[self.resource]

    def test_jsonpath_search_nested_string(self):
        resources = (
            ('resource1', {'foo': TEST_DICT}),
            ('resource2', {'foo': TEST_STRING})
        )
        created = self.setup_resources(resources)

        found = self.get_resources(vars='foo.baz:zoo')

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
