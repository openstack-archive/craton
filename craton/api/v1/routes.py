from craton.api.v1.inventory.cells import Cells
from craton.api.v1.inventory.cells import CellById
from craton.api.v1.inventory.cells import CellsData
from craton.api.v1.inventory.hosts import Hosts
from craton.api.v1.inventory.hosts import HostById
from craton.api.v1.inventory.hosts import HostsData
from craton.api.v1.inventory.regions import Regions
from craton.api.v1.inventory.regions import RegionsById
from craton.api.v1.inventory.regions import RegionsData


routes = [
    dict(resource=HostsData,
         urls=['/hosts/<id>/data'],
         endpoint='hosts_data'),
    dict(resource=HostById,
         urls=['/hosts/<id>'],
         endpoint='hosts_id'),
    dict(resource=Hosts,
         urls=['/hosts'],
         endpoint='hosts'),
    dict(resource=Regions,
         urls=['/regions'],
         endpoint='regions'),
    dict(resource=RegionsById,
         urls=['/regions/<id>'],
         endpoint='regions_id'),
    dict(resource=RegionsData,
         urls=['/regions/<id>/data'],
         endpoint='regions_data'),
    dict(resource=CellById,
         urls=['/cells/<id>'],
         endpoint='cells_id'),
    dict(resource=Cells,
         urls=['/cells'],
         endpoint='cells'),
    dict(resource=CellsData,
         urls=['/cells/<id>/data'],
         endpoint='cells_data'),
]
