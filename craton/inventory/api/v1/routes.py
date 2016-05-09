from craton.inventory.api.v1.cells import Cells
from craton.inventory.api.v1.cells import CellsId
from craton.inventory.api.v1.cells import CellsData
from craton.inventory.api.v1.hosts import Hosts
from craton.inventory.api.v1.hosts import HostsId
from craton.inventory.api.v1.hosts import HostsData
from craton.inventory.api.v1.regions import Regions
from craton.inventory.api.v1.regions import RegionsId
from craton.inventory.api.v1.regions import RegionsData


routes = [
    dict(resource=HostsData,
         urls=['/hosts/<id>/data'],
         endpoint='hosts_data'),
    dict(resource=HostsId,
         urls=['/hosts/<id>'],
         endpoint='hosts_id'),
    dict(resource=Hosts,
         urls=['/hosts'],
         endpoint='hosts'),
    dict(resource=Regions,
         urls=['/regions'],
         endpoint='regions'),
    dict(resource=RegionsId,
         urls=['/regions/<id>'],
         endpoint='regions_id'),
    dict(resource=RegionsData,
         urls=['/regions/<id>/data'],
         endpoint='regions_data'),
    dict(resource=Cells,
         urls=['/cells/<id>'],
         endpoint='cells_id'),
    dict(resource=Cells,
         urls=['/cells'],
         endpoint='cells'),
    dict(resource=CellsData,
         urls=['/cells/<id>/data'],
         endpoint='cells_data'),
]
