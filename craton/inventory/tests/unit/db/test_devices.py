from netaddr import IPAddress

from craton.inventory.db import api as dbapi
from craton.inventory.tests.unit.db import base


class HostsDBTestCase(base.DBTestCase):

    project_id = 42

    def make_region(self, name, **variables):
        region = dbapi.regions_create(
            self.context,
            {'name': name,
             'project_id': self.project_id,
             'variables': variables})
        return region.id

    def make_cell(self, region_id, name, **variables):
        cell = dbapi.cells_create(
            self.context,
            {'name': name,
             'project_id': self.project_id,
             'region_id': region_id,
             'variables': variables})
        return cell.id

    def make_host(self, region_id, cell_id, name, ip_address,
                  host_type, parent_id=None, labels=None, **variables):
        host = dbapi.hosts_create(
            self.context,
            {'name': name,
             'project_id': self.project_id,
             'region_id': region_id,
             'parent_id': parent_id,
             'device_type': host_type,
             'cell_id': cell_id,
             'ip_address': ip_address,
             'active': True,
             'labels': set() if labels is None else labels,
             'variables': variables})
        return host.id

    def test_hosts_create(self):
        region_id = self.make_region(
            'region_1',
            foo='R1', bar='R2', bax='R3')
        cell_id = self.make_cell(region_id, 'cell_1', bar='C2')
        host_id = self.make_host(
            region_id, cell_id, 'www1.example.com',
            IPAddress(u'10.1.2.101'),
            'server',
            foo='H1', baz='H3')

        # Need to do this query despite creation above because other
        # elements (cell, region) were in separate committed sessions
        # when the host was created. Verify these linked elements load
        # correctly
        host = dbapi.hosts_get_by_id(self.context, host_id)
        self.assertEqual(host.region.id, region_id)
        self.assertEqual(host.region.name, 'region_1')
        self.assertEqual(host.cell.id, cell_id)
        self.assertEqual(host.cell.name, 'cell_1')

        # Verify resolved variables/blames override properly
        self.assertEqual(
            host.resolved,
            {'foo': 'H1', 'bar': 'C2', 'baz': 'H3', 'bax': 'R3'})

        blame = dbapi.device_blame_variables(host, ['foo', 'bar'])
        self.assertEqual(blame['foo'].source.name, 'www1.example.com')
        self.assertEqual(blame['foo'].variable.value, 'H1')
        self.assertEqual(blame['bar'].source.name, 'cell_1')
        self.assertEqual(blame['bar'].variable.value, 'C2')
