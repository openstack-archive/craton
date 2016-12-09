from craton.api.v1.resources import users
from craton.api.v1.resources import projects

from craton.api.v1.resources.inventory import ansible_inventory
from craton.api.v1.resources.inventory import cells
from craton.api.v1.resources.inventory import hosts
from craton.api.v1.resources.inventory import regions
from craton.api.v1.resources.inventory import networks


routes = [
    dict(resource=ansible_inventory.AnsibleInventory,
         urls=['/ansible_inventory'],
         endpoint='ansible_inventory'),
    dict(resource=hosts.HostsVariables,
         urls=['/hosts/<id>/variables'],
         endpoint='hosts_id_variables'),
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
    dict(resource=regions.RegionsVariables,
         urls=['/regions/<id>/variables'],
         endpoint='regions_id_variables'),
    dict(resource=cells.CellById,
         urls=['/cells/<id>'],
         endpoint='cells_id'),
    dict(resource=cells.Cells,
         urls=['/cells'],
         endpoint='cells'),
    dict(resource=cells.CellsVariables,
         urls=['/cells/<id>/variables'],
         endpoint='cells_id_variables'),
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
    dict(resource=networks.NetworksVariables,
         urls=['/networks/<id>/variables'],
         endpoint='networks_id_variables'),
    dict(resource=networks.NetworkById,
         urls=['/networks/<id>'],
         endpoint='networks_id'),
    dict(resource=networks.NetworkInterfaces,
         urls=['/network_interfaces'],
         endpoint='network_interfaces'),
    dict(resource=networks.NetworkInterfaceById,
         urls=['/network_interfaces/<id>'],
         endpoint='network_interfaces_id'),
    dict(resource=networks.NetworkDevices,
         urls=['/network_devices'],
         endpoint='network_devices'),
    dict(resource=networks.NetworkDeviceById,
         urls=['/network_devices/<id>'],
         endpoint='network_devices_id'),
    dict(resource=networks.NetworkDevicesVariables,
         urls=['/network_devices/<id>/variables'],
         endpoint='network_devices_id_variables'),
    dict(resource=networks.NetworkDeviceLabels,
         urls=['/network_devices/<id>/labels'],
         endpoint='network_devices_labels'),
]
