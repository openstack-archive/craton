from craton.inventory.api.v1.cells import Cells
from craton.inventory.api.v1.cells import CellById
from craton.inventory.api.v1.cells import CellsData
from craton.inventory.api.v1.hosts import Hosts
from craton.inventory.api.v1.hosts import HostById
from craton.inventory.api.v1.hosts import HostsData
from craton.inventory.api.v1.regions import Regions
from craton.inventory.api.v1.regions import RegionsById
from craton.inventory.api.v1.regions import RegionsData


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
