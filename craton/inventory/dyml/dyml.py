import yaml, pprint
from plugins import core, kir

class dyml_obj(object):
   def __init__(self):
      yaml.add_constructor(u'!core_query_device',self._core_query_device)
      yaml.add_constructor(u'!kir_query_url', self._kir_query_url)
      self.data = {}

   def _core_query_device(self,loader,node):
      device = loader.construct_sequence(node)[0]
      attribute = loader.construct_sequence(node)[1]

      return core.query_device(device,attribute)

   def _kir_query_url(self,loader,node):
      dc = loader.construct_sequence(node)[0]
      device = loader.construct_sequence(node)[1]

      return kir.query_url(dc,device)

   def load_dyml(self,filename):
       with open(filename) as data_file:
          self.data =yaml.load(data_file)

   def dump_yml(self,filename):
       with open(filename, 'w') as outfile:
        yaml.dump(self.data, outfile, default_flow_style=False)

   def __repr__(self):
       return pprint.pformat(self.data)
