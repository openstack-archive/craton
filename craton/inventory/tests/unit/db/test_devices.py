from netaddr import IPAddress

from craton.inventory.db import api as dbapi
from craton.inventory.tests.unit.db import base


def make_region(context, name, project_id, variables):
    region = dbapi.regions_create(
        context,
        {'name': name,
         'project_id': project_id})
    dbapi.regions_data_update(context, region.id, variables)
    return region.id


def make_cell(context, name, project_id, region_id, variables):
    cell = dbapi.cells_create(
        context,
        {'name': name,
         'project_id': project_id,
         'region_id': region_id})
    dbapi.cells_data_update(context, cell.id, variables)
    return cell.id


def make_host(context, name, region_id, variables):
    host = dbapi.hosts_create(
        context, {'name': name, 'region_id': region_id})
    dbapi.cells_data_update(context, host.id, variables)
    return host.id


class HostsDBTestCase(base.DBTestCase):

    def test_hosts_create(self):
        region3 = {'id': 3, 'project_id': 2,
                   'name': 'region3',
                   'variables': {'foo': 'R1',
                                 'bar': 'R2',
                                 'bax': 'R3'}}
        dbapi.regions_create(self.context, region3)
        cell5 = {'id': 5, 'project_id': 2, 'region_id': 3,
                 'name': 'cell5',
                 'variables': {'bar': 'C2'}}
        dbapi.cells_create(self.context, cell5)
        host7 = {
            'id': 7, 'project_id': 2, 'region_id': 3, 'cell_id': 5,
            'name': 'www1.example.com',
            'ip_address': IPAddress(u'10.1.2.101'),
            'active': True,
            'labels': set(),  # TODO(jimbaker) add actual labels
            'variables': {'foo': 'H1', 'baz': 'H3'}}
        dbapi.hosts_create(self.context, host7)

        # Need to do this query despite creation above because other
        # elements (cell, region) were in separate committed sessions
        # when the host was created. Verify these linked elements are loaded:

        host = dbapi.hosts_get_by_id(self.context, 7)
        self.assertEqual(host.region.id, 3)
        self.assertEqual(host.region.name, 'region3')
        self.assertEqual(host.cell.id, 5)
        self.assertEqual(host.cell.name, 'cell5')

        # As well as resolved variables
        self.assertEqual(
            host.resolved,
            {'foo': 'H1', 'bar': 'C2', 'baz': 'H3', 'bax': 'R3'})
