from craton.api.v1.resources import users
from craton.api.v1.resources import projects
from craton.api.v1.resources import variables

from craton.api.v1.resources.inventory import ansible_inventory
from craton.api.v1.resources.inventory import cells
from craton.api.v1.resources.inventory import clouds
from craton.api.v1.resources.inventory import hosts
from craton.api.v1.resources.inventory import regions
from craton.api.v1.resources.inventory import networks


VARS_RESOLVE = ", ".join(map(repr, ("hosts", )))
VARS_NOT_RESOLVE = ", ".join(
    map(repr, ("network-devices", "cells", "regions", "networks", "projects",
               "clouds"))
)

routes = [
    dict(resource=ansible_inventory.AnsibleInventory,
         urls=['/ansible-inventory'],
         endpoint='ansible_inventory'),
    dict(resource=hosts.HostsLabels,
         urls=['/hosts/<id>/labels'],
         endpoint='hosts_labels'),
    dict(resource=hosts.HostById,
         urls=['/hosts/<id>'],
         endpoint='hosts_id'),
    dict(resource=hosts.Hosts,
         urls=['/hosts'],
         endpoint='hosts'),
    dict(resource=regions.Regions,
         urls=['/regions'],
         endpoint='regions'),
    dict(resource=regions.RegionsById,
         urls=['/regions/<id>'],
         endpoint='regions_id'),
    dict(resource=clouds.Clouds,
         urls=['/clouds'],
         endpoint='clouds'),
    dict(resource=clouds.CloudsById,
         urls=['/clouds/<id>'],
         endpoint='clouds_id'),
    dict(resource=cells.CellById,
         urls=['/cells/<id>'],
         endpoint='cells_id'),
    dict(resource=cells.Cells,
         urls=['/cells'],
         endpoint='cells'),
    dict(resource=projects.Projects,
         urls=['/projects'],
         endpoint='projects'),
    dict(resource=projects.ProjectById,
         urls=['/projects/<id>'],
         endpoint='projects_id'),
    dict(resource=users.Users,
         urls=['/users'],
         endpoint='users'),
    dict(resource=users.UserById,
         urls=['/users/<id>'],
         endpoint='users_id'),
    dict(resource=networks.Networks,
         urls=['/networks'],
         endpoint='networks'),
    dict(resource=networks.NetworkById,
         urls=['/networks/<id>'],
         endpoint='networks_id'),
    dict(resource=networks.NetworkInterfaces,
         urls=['/network-interfaces'],
         endpoint='network_interfaces'),
    dict(resource=networks.NetworkInterfaceById,
         urls=['/network-interfaces/<id>'],
         endpoint='network_interfaces_id'),
    dict(resource=networks.NetworkDevices,
         urls=['/network-devices'],
         endpoint='network_devices'),
    dict(resource=networks.NetworkDeviceById,
         urls=['/network-devices/<id>'],
         endpoint='network_devices_id'),
    dict(resource=networks.NetworkDeviceLabels,
         urls=['/network-devices/<id>/labels'],
         endpoint='network_devices_labels'),
    dict(resource=variables.Variables,
         urls=['/<any({}):resources>/<id>/variables'.format(VARS_RESOLVE)],
         endpoint='variables_with_resolve'),
    dict(resource=variables.Variables,
         urls=['/<any({}):resources>/<id>/variables'.format(VARS_NOT_RESOLVE)],
         endpoint='variables_without_resolve'),
]
