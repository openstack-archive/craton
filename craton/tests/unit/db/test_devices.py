import uuid

from netaddr import IPAddress

from craton import exceptions
from craton.db import api as dbapi
from craton.tests.unit.db import base

default_pagination = {'limit': 30, 'marker': None}


class HostsDBTestCase(base.DBTestCase):

    mock_project_id = uuid.uuid4().hex

    def make_project(self, name, **variables):
        project = dbapi.projects_create(
            self.context,
            {"name": name,
             "variables": variables})
        return str(project.id)

    def make_region(self, project_id, name, **variables):
        region = dbapi.regions_create(
            self.context,
            {'name': name,
             'project_id': project_id,
             'variables': variables})
        return region.id

    def make_cell(self, project_id, region_id, name, **variables):
        cell = dbapi.cells_create(
            self.context,
            {'name': name,
             'project_id': project_id,
             'region_id': region_id,
             'variables': variables})
        return cell.id

    def make_host(self, project_id, region_id, name, ip_address, host_type,
                  cell_id=None, parent_id=None, labels=None, **variables):
        if cell_id:
            host = {'name': name,
                    'project_id': project_id,
                    'region_id': region_id,
                    'cell_id': cell_id,
                    'ip_address': ip_address,
                    'parent_id': parent_id,
                    'device_type': host_type,
                    'active': True,
                    'labels': set() if labels is None else labels,
                    'variables': variables}
        else:
            host = {'name': name,
                    'project_id': project_id,
                    'region_id': region_id,
                    'ip_address': ip_address,
                    'parent_id': parent_id,
                    'device_type': host_type,
                    'active': True,
                    'labels': set() if labels is None else labels,
                    'variables': variables}

        host = dbapi.hosts_create(self.context, host)
        return host.id

    def make_very_small_cloud(self, with_cell=False):
        project_id = self.make_project('project_1', foo='P1', zoo='P2')
        region_id = self.make_region(
            project_id,
            'region_1',
            foo='R1', bar='R2', bax='R3')
        if with_cell:
            cell_id = self.make_cell(project_id, region_id, 'cell_1', bar='C2')
        else:
            cell_id = None
        host_id = self.make_host(project_id, region_id, 'www1.example.com',
                                 IPAddress(u'10.1.2.101'), 'server',
                                 cell_id=cell_id, foo='H1', baz='H3')
        return project_id, region_id, cell_id, host_id

    def test_hosts_create(self):
        # Need to do this query despite creation above because other
        # elements (cell, region) were in separate committed sessions
        # when the host was created. Verify these linked elements load
        # correctly
        project_id, region_id, cell_id, host_id = self.make_very_small_cloud(
            with_cell=True)
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(host.region.id, region_id)
        self.assertEqual(host.region.name, 'region_1')
        self.assertEqual(host.cell.id, cell_id)
        self.assertEqual(host.cell.name, 'cell_1')

        # Verify resolved variables/blames override properly
        self.assertEqual(
            [obj.id for obj in host.resolution_order],
            [host_id, cell_id, region_id, uuid.UUID(project_id)])

        self.assertEqual(
            [variables for variables in host.resolution_order_variables],
            [{'foo': 'H1', 'baz': 'H3'},
             {'bar': 'C2'},
             {'foo': 'R1', 'bar': 'R2', 'bax': 'R3'},
             {'foo': 'P1', 'zoo': 'P2'}])

        self.assertEqual(
            host.resolved,
            {'foo': 'H1', 'bar': 'C2', 'baz': 'H3', 'bax': 'R3', 'zoo': 'P2'})

        blame = host.blame(['foo', 'bar', 'zoo'])
        self.assertEqual(blame['foo'].source.name, 'www1.example.com')
        self.assertEqual(blame['foo'].variable.value, 'H1')
        self.assertEqual(blame['bar'].source.name, 'cell_1')
        self.assertEqual(blame['bar'].variable.value, 'C2')
        self.assertEqual(blame['zoo'].source.name, 'project_1')
        self.assertEqual(blame['zoo'].variable.value, 'P2')

    def test_hosts_create_duplicate_raises(self):
        region_id = self.make_region(self.mock_project_id, 'region_1')
        self.make_host(self.mock_project_id, region_id, 'www1.example.com',
                       IPAddress(u'10.1.2.101'), 'server')
        new_host = {'name': 'www1.example.com', 'region_id': region_id,
                    'ip_address': IPAddress(u'10.1.2.101'),
                    'device_type': 'server',
                    'project_id': self.mock_project_id}
        self.assertRaises(exceptions.DuplicateDevice, dbapi.hosts_create,
                          self.context, new_host)

    def test_hosts_create_without_cell(self):
        project_id, region_id, _, host_id = self.make_very_small_cloud()
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(host.region.id, region_id)
        self.assertEqual(host.region.name, 'region_1')
        self.assertIsNone(host.cell)

        # Verify resolved variables/blames override properly
        self.assertEqual(
            [obj.id for obj in host.resolution_order],
            [host_id, region_id, uuid.UUID(project_id)])

        self.assertEqual(
            [variables for variables in host.resolution_order_variables],
            [{'foo': 'H1', 'baz': 'H3'},
             {'foo': 'R1', 'bar': 'R2', 'bax': 'R3'},
             {'foo': 'P1', 'zoo': 'P2'}])

        self.assertEqual(
            host.resolved,
            {'foo': 'H1', 'bar': 'R2', 'baz': 'H3', 'bax': 'R3', 'zoo': 'P2'})

        blame = host.blame(['foo', 'bar', 'zoo'])
        self.assertEqual(blame['foo'].source.name, 'www1.example.com')
        self.assertEqual(blame['foo'].variable.value, 'H1')
        self.assertEqual(blame['bar'].source.name, 'region_1')
        self.assertEqual(blame['bar'].variable.value, 'R2')
        self.assertEqual(blame['zoo'].source.name, 'project_1')
        self.assertEqual(blame['zoo'].variable.value, 'P2')

    def test_hosts_update(self):
        region_id = self.make_region(self.mock_project_id, 'region_1')
        host_id = self.make_host(self.mock_project_id, region_id, 'example',
                                 IPAddress(u'10.1.2.101'), 'server',
                                 bar='bar2')
        name = "Host_New"
        res = dbapi.hosts_update(self.context, host_id, {'name': 'Host_New'})
        self.assertEqual(res.name, name)

    def test_hosts_variable_resolved_with_parent(self):
        project_id = self.make_project(
            'project_1',
            foo='P1', zoo='P2')
        region_id = self.make_region(
            project_id,
            'region_1',
            foo='R1', bar='R2', bax='R3')
        cell_id = self.make_cell(project_id, region_id, 'cell_1',
                                 bar='C2')
        host1_id = self.make_host(project_id, region_id, 'www1.example.com',
                                  IPAddress(u'10.1.2.101'), 'server',
                                  cell_id=cell_id, foo='H1', baz='H3')
        host2_id = self.make_host(project_id, region_id, 'www1.example2.com',
                                  IPAddress(u'10.1.2.102'), 'server',
                                  cell_id=cell_id, parent_id=host1_id)
        host2 = dbapi.hosts_get_by_id(self.context, host2_id)

        # Verify resolved variables/blames override properly
        self.assertEqual(
            [obj.id for obj in host2.resolution_order],
            [host2_id, host1_id, cell_id, region_id, uuid.UUID(project_id)])

        self.assertEqual(
            [variables for variables in host2.resolution_order_variables],
            [{},
             {'baz': 'H3', 'foo': 'H1'},
             {'bar': 'C2'},
             {'bar': 'R2', 'foo': 'R1', 'bax': 'R3'},
             {'foo': 'P1', 'zoo': 'P2'}])

        self.assertEqual(
            host2.resolved,
            {'foo': 'H1', 'bar': 'C2', 'baz': 'H3', 'bax': 'R3', 'zoo': 'P2'})

        blame = host2.blame(['foo', 'bar', 'zoo'])
        self.assertEqual(blame['foo'].source.name, 'www1.example.com')
        self.assertEqual(blame['foo'].variable.value, 'H1')
        self.assertEqual(blame['bar'].source.name, 'cell_1')
        self.assertEqual(blame['bar'].variable.value, 'C2')
        self.assertEqual(blame['zoo'].source.name, 'project_1')
        self.assertEqual(blame['zoo'].variable.value, 'P2')

    def test_hosts_variables_no_resolved(self):
        project_id = self.make_project('project_1', zoo='P2')
        region_id = self.make_region(project_id, 'region_1', foo='R1')
        host_id = self.make_host(project_id, region_id, 'www.example.xyz',
                                 IPAddress(u'10.1.2.101'),
                                 'server', bar='bar2')
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(host.name, 'www.example.xyz')
        self.assertEqual(host.variables, {'bar': 'bar2'})

    def test_hosts_resolved_vars_no_cells(self):
        project_id = self.make_project('project_1')
        region_id = self.make_region(project_id, 'region_1',
                                     foo='R1')
        host_id = self.make_host(project_id, region_id,
                                 'www.example.xyz',
                                 IPAddress(u'10.1.2.101'),
                                 'server', bar='bar2')
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(host.name, 'www.example.xyz')
        self.assertEqual(host.resolved, {'bar': 'bar2', 'foo': 'R1'})

    def test_host_labels_create(self):
        region_id = self.make_region(self.mock_project_id, 'region_1',
                                     foo='R1')
        host_id = self.make_host(self.mock_project_id, region_id,
                                 'www.example.xyz',
                                 IPAddress(u'10.1.2.101'),
                                 'server', bar='bar2')
        labels = {"labels": ["tom", "jerry"]}
        dbapi.hosts_labels_update(self.context, host_id, labels)

    def test_host_labels_delete(self):
        region_id = self.make_region(self.mock_project_id, 'region_1',
                                     foo='R1')
        host_id = self.make_host(self.mock_project_id, region_id,
                                 'www.example.xyz',
                                 IPAddress(u'10.1.2.101'),
                                 'server', bar='bar2')
        _labels = {"labels": ["tom", "jerry", "jones"]}
        dbapi.hosts_labels_update(self.context, host_id, _labels)
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(sorted(host.labels), sorted(_labels["labels"]))
        _dlabels = {"labels": ["tom"]}
        dbapi.hosts_labels_delete(self.context, host_id, _dlabels)
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(host.labels, {"jerry", "jones"})

    def test_hosts_get_all_with_filter_cell_id(self):
        project_id = self.make_project('project_1', foo='P1', zoo='P2')
        region_id = self.make_region(project_id, 'region_1', foo='R1')
        cell_id1 = self.make_cell(project_id, region_id, 'cell_1', bar='C2')
        cell_id2 = self.make_cell(project_id, region_id, 'cell_2', bar='C2')
        self.assertNotEqual(cell_id1, cell_id2)

        self.make_host(
            project_id,
            region_id,
            'www.example.xyz',
            IPAddress(u'10.1.2.101'),
            'server',
            cell_id=cell_id1,
        )
        self.make_host(
            project_id,
            region_id,
            'www.example.abc',
            IPAddress(u'10.1.2.102'),
            'server',
            cell_id=cell_id2,
        )

        all_res = dbapi.hosts_get_all(self.context, {}, default_pagination)
        self.assertEqual(len(all_res), 2)
        self.assertEqual(
            len([host for host in all_res if host['cell_id'] == cell_id1]), 1
        )

        filters = {
            "cell_id": cell_id1,
        }
        res = dbapi.hosts_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, 'www.example.xyz')

    def test_hosts_get_all_with_filters(self):
        project_id = self.make_project('project_1', foo='P1', zoo='P2')
        region_id = self.make_region(project_id, 'region_1', foo='R1')
        host_id = self.make_host(project_id, region_id, 'www.example.xyz',
                                 IPAddress(u'10.1.2.101'),
                                 'server')
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.variables_update_by_resource_id(
            self.context, "hosts", host_id, variables
        )
        filters = {
            "region_id": region_id,
            "vars": "key2:value2",
        }
        res = dbapi.hosts_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, 'www.example.xyz')

    def test_hosts_get_with_key_value_filters(self):
        project_id = self.make_project('project_1', foo='P1', zoo='P2')
        region_id = self.make_region(project_id, 'region_1', foo='R1')
        host1 = self.make_host(project_id, region_id, 'www.example.xyz',
                               IPAddress(u'10.1.2.101'),
                               'server')
        variables = {"key1": "example1", "key2": "Tom"}
        dbapi.variables_update_by_resource_id(
            self.context, "hosts", host1, variables
        )
        # Second host with own variables
        host2 = self.make_host(project_id, region_id, 'www.example2.xyz',
                               IPAddress(u'10.1.2.102'),
                               'server')
        variables = {"key1": "example2", "key2": "Tom"}
        dbapi.variables_update_by_resource_id(
            self.context, "hosts", host2, variables
        )
        filters = {"vars": "key1:example2"}

        res = dbapi.hosts_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 1)
        self.assertEqual('www.example2.xyz', res[0].name)

        filters = {"vars": "key2:Tom"}
        res = dbapi.hosts_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 2)

    def test_hosts_get_all_with_filters_noexist(self):
        project_id = self.make_project('project_1', foo='P1', zoo='P2')
        region_id = self.make_region(project_id, 'region_1', foo='R1')
        host_id = self.make_host(project_id, region_id, 'www.example.xyz',
                                 IPAddress(u'10.1.2.101'),
                                 'server')
        variables = {"key1": "value1", "key2": "value2"}
        dbapi.variables_update_by_resource_id(
            self.context, "hosts", host_id, variables
        )
        filters = {
            "region_id": "region_1",
            "vars": "key1:value5",
        }
        res = dbapi.hosts_get_all(self.context, filters, default_pagination)
        self.assertEqual(len(res), 0)
