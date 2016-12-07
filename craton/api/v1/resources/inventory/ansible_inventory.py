from collections import OrderedDict
from flask import g
from flask import request
from operator import attrgetter
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class AnsibleInventory(base.Resource):

    def get_hierarchy(self, devices):
        regions = set()
        cells = set()
        labels = set()

        for device in devices:
            if device.region not in regions:
                regions.add(device.region)

            if device.cell:
                if device.cell not in cells:
                    cells.add(device.cell)
            for label in device.labels:
                if label not in labels:
                    labels.add(label)

        regions = sorted(regions, key=attrgetter('name'))
        cells = sorted(cells, key=attrgetter('name'))
        labels = sorted(labels, key=attrgetter('label'))
        devices = sorted(devices, key=attrgetter('ip_address'))
        return regions, cells, labels, devices

    def generate_ansible_inventory(self, hosts):
        """Generate and return Ansible inventory in json format
        for hosts given by provided filters.
        """
        regions, cells, labels, hosts = self.get_hierarchy(hosts)
        hosts_set = set(hosts)
        # Set group 'all' and set '_meta'
        inventory = OrderedDict(
            [('all', {'hosts': []}),
             ('_meta', {'hostvars': OrderedDict()})]
        )

        for host in hosts:
            ip = str(host.ip_address)
            inventory['all']['hosts'].append(ip)
            inventory['_meta']['hostvars'][ip] = host.resolved

        def matching_hosts(obj):
            return sorted(
                [str(device.ip_address) for device in obj.devices
                 if device in hosts_set])

        # Group hosts by label
        # TODO(sulo): make sure we have a specified label to
        # identify host group. Fix this after label refractoring.
        for label in labels:
            inventory[label.label] = {
                'hosts': matching_hosts(label),
                'vars': label.variables
            }

        for cell in cells:
            inventory['%s-%s' % (cell.region.name, cell.name)] = {
                'hosts': matching_hosts(cell),
                'vars': cell.variables
            }

        for region in regions:
            ch = ['%s-%s' % (region.name, cell.name) for cell in region.cells]
            inventory['%s' % region.name] = {
                'children': ch,
                'vars': region.variables
            }
        return inventory

    def get(self):
        context = request.environ.get("context")
        region_id = g.args["region_id"]
        cell_id = g.args["cell_id"]

        filters = {}
        if region_id:
            filters['region_id'] = region_id

        # TODO(sulo): allow other filters based on services
        if cell_id:
            filters['cell_id'] = cell_id

        try:
            hosts_obj = dbapi.hosts_get_all(context, filters)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during host get: %s" % err)
            return self.error_response(500, 'Unknown Error')

        _inventory = self.generate_ansible_inventory(hosts_obj)
        inventory = jsonutils.to_primitive(_inventory)
        return inventory, 200, None
