import six


DefinitionsHost = {'discriminator': 'name',
                   'required': ['name',
                                'region_id',
                                'project_id',
                                'ip_address',
                                'device_type'],
                   'type': 'object',
                   'properties': {
                       'active': {'type': 'boolean'},
                       'note': {'type': 'string'},
                       'ip_address': {'type': 'string'},
                       'name': {'type': 'string'},
                       'id': {'type': 'integer'},
                       'cell_id': {'type': 'integer'},
                       'project_id': {'type': 'integer'},
                       'parent_id': {'type': 'integer',
                                     'description': 'Parent Id of this host'},
                       'device_type': {'type': 'string',
                                       'description': 'Type of host'},
                       'labels': {'type': 'allOf',
                                  'description': 'User defined labels'},
                       'data': {'type': 'allOf',
                                'description': 'User defined information'},
                       'region_id': {'type': 'integer'}}}

DefinitionsHostId = {'discriminator': 'name',
                     'type': 'object',
                     'properties': {
                         'active': {'type': 'boolean'},
                         'note': {'type': 'string'},
                         'ip_address': {'type': 'string'},
                         'name': {'type': 'string'},
                         'id': {'type': 'integer'},
                         'cell_id': {'type': 'integer'},
                         'project_id': {'type': 'integer'},
                         'labels': {'type': 'allOf',
                                    'description': 'User defined labels'},
                         'data': {'type': 'allOf',
                                  'description': 'User defined information'},
                         'region_id': {'type': 'integer'}}}

DefinitionsCell = {'discriminator': 'name',
                   'required': ['name',
                                'region_id',
                                'project_id'
                                ],
                   'type': 'object',
                   'properties': {
                       'note': {'type': 'string'},
                       'project_id': {'type': 'integer',
                                      'description': 'ID of the project'},
                       'name': {'type': 'string'},
                       'region_id': {'type': 'integer'},
                       'data': {'type': 'allOf',
                                'description': 'User defined information'},
                       'id': {'type': 'integer',
                              'description': 'Unique ID of the cell'}}}

DefinitionsCellId = {'discriminator': 'name',
                     'type': 'object',
                     'properties': {
                         'note': {'type': 'string'},
                         'project_id': {'type': 'integer',
                                        'description': 'ID of the project'},
                         'name': {'type': 'string'},
                         'region_id': {'type': 'integer'},
                         'data': {'type': 'allOf',
                                  'description': 'User defined information'},
                         'id': {'type': 'integer',
                                'description': 'Unique ID of the cell'}}}

DefinitionsData = {'type': 'object',
                   'properties': {'key': {'type': 'string'},
                                  'value': {'type': 'object'}}}

DefinitionsError = {'type': 'object',
                    'properties': {'fields': {'type': 'string'},
                                   'message': {'type': 'string'},
                                   'code': {'type': 'integer',
                                            'format': 'int32'}
                                   }}

DefinitionsRegion = {'discriminator': 'name',
                     'required': ['name'],
                     'type': 'object',
                     'properties': {
                         'note': {
                             'type': 'string',
                             'description': 'Region Note'},
                         'name': {
                             'type': 'string',
                             'description': 'Region Name.'},
                         'project_id': {
                             'type': 'integer',
                             'description': 'ID of the project'},
                         'cells': {
                             'items': DefinitionsCell,
                             'type': 'array',
                             'description': 'List of cells in this region'},
                         'data': {
                             'type': 'allOf',
                             'description': 'User defined information'},
                         'id': {
                             'type': 'integer',
                             'description': 'Unique ID for the region.'}}}

DefinitionsRegionId = {'discriminator': 'name',
                       'type': 'object',
                       'properties': {
                           'note': {
                               'type': 'string',
                               'description': 'Region Note'},
                           'name': {
                               'type': 'string',
                               'description': 'Region Name.'},
                           'project_id': {
                               'type': 'integer',
                               'description': 'ID of the project'},
                           'cells': {
                               'items': DefinitionsCell,
                               'type': 'array',
                               'description': 'List of cells in this region'},
                           'data': {
                               'type': 'allOf',
                               'description': 'User defined information'},
                           'id': {
                               'type': 'integer',
                               'description': 'Unique ID for the region.'}}}

DefinitionUser = {'discriminator': 'name',
                  'type': 'object',
                  'properties': {
                      'id': {'type': 'integer'},
                      'api_key': {'type': 'string'},
                      'username': {'type': 'string'},
                      'is_admin': {'type': 'boolean'},
                      'project_id': {'type': 'integer'},
                      'roles': {'type': 'allOf'}}}

DefinitionProject = {'discriminator': 'name',
                     'type': 'object',
                     'properties': {
                         'id': {'type': 'integer'},
                         'name': {'type': 'string'}}}

DefinitionNetwork = {'discriminator': 'name',
                     'required': ['name',
                                  'project_id',
                                  'cidr',
                                  'gateway',
                                  'netmask'],
                     'type': 'object',
                     'properties': {
                         'id': {'type': 'integer'},
                         'project_id': {'type': 'integer'},
                         'region_id': {'type': 'integer'},
                         'cell_id': {'type': 'integer'},
                         'name': {'type': 'string'},
                         'cidr': {'type': 'string'},
                         'gateway': {'type': 'string'},
                         'netmask': {'type': 'string'},
                         'data': {'type': 'allOf'},
                         "ip_block_type": {'type': 'string'},
                         "nss": {'type': 'string'}}}

DefinitionNetworkId = {'discriminator': 'name',
                       'type': 'object',
                       'properties': {
                           'id': {'type': 'integer'},
                           'project_id': {'type': 'integer'},
                           'region_id': {'type': 'integer'},
                           'cell_id': {'type': 'integer'},
                           'name': {'type': 'string'},
                           'cidr': {'type': 'string'},
                           'gateway': {'type': 'string'},
                           'netmask': {'type': 'string'},
                           'data': {'type': 'allOf'},
                           "ip_block_type": {'type': 'string'},
                           "nss": {'type': 'string'}}}

DefinitionNetInterface = {'discriminator': 'name',
                          'required': ['name',
                                       'device_id',
                                       'interface_type'],
                          'type': 'object',
                          'properties': {
                              'id': {'type': 'integer'},
                              'name': {'type': 'string'},
                              'device_id': {'type': 'integer',
                                            'default': None},
                              'network_id': {'type': 'integer',
                                             'default': None},
                              'interface_type': {'type': 'string'},
                              'vlan_id': {'type': 'integer'},
                              'vlan': {'type': 'string'},
                              'port': {'type': 'string'},
                              'duplex': {'type': 'string'},
                              'speed': {'type': 'integer'},
                              'link': {'type': 'string'},
                              'cdp': {'type': 'string'},
                              'data': {'type': 'allOf'},
                              'security': {'type': 'string'}}}

DefinitionNetInterfaceId = {'discriminator': 'name',
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'device_id': {'type': 'integer'},
                                'network_id': {'type': 'integer'},
                                'interface_type': {'type': 'string'},
                                'vlan_id': {'type': 'integer'},
                                'vlan': {'type': 'string'},
                                'port': {'type': 'string'},
                                'duplex': {'type': 'string'},
                                'speed': {'type': 'integer'},
                                'link': {'type': 'string'},
                                'cdp': {'type': 'string'},
                                'data': {'type': 'allOf'},
                                'security': {'type': 'string'}}}

DefinitionNetDevice = {'discriminator': 'hostname',
                       'required': ['hostname',
                                    'region_id',
                                    'project_id',
                                    'device_type',
                                    'ip_address'],
                       'type': 'object',
                       'properties': {
                           'id': {'type': 'integer'},
                           'project_id': {'type': 'integer'},
                           'region_id': {'type': 'integer'},
                           'cell_id': {'type': 'integer'},
                           'parent_id': {'type': 'integer'},
                           'ip_address': {'type': 'string'},
                           'device_type': {'type': 'string'},
                           'hostname': {'type': 'string'},
                           'access_secret_id': {'type': 'integer'},
                           'model_name': {'type': 'string'},
                           'os_version': {'type': 'string'},
                           'vlans': {'type': 'string'},
                           'data': {'type': 'allOf',
                                    'description': 'User defined variables'},
                           'interface_id': {'type': 'integer'},
                           'network_id': {'type': 'integer'}}}

DefinitionNetDeviceId = {'discriminator': 'hostname',
                         'type': 'object',
                         'properties': {
                             'id': {'type': 'integer'},
                             'project_id': {'type': 'integer'},
                             'region_id': {'type': 'integer'},
                             'cell_id': {'type': 'integer'},
                             'parent_id': {'type': 'integer'},
                             'ip_address': {'type': 'string'},
                             'device_type': {'type': 'string'},
                             'hostname': {'type': 'string'},
                             'access_secret_id': {'type': 'integer'},
                             'model_name': {'type': 'string'},
                             'os_version': {'type': 'string'},
                             'vlans': {'type': 'string'},
                             'interface_id': {'type': 'integer'},
                             'data': {'type': 'allOf',
                                      'description': 'User defined variables'},
                             'network_id': {'type': 'integer'}}}


validators = {
    ('ansible_inventory', 'GET'): {
        'args': {'required': ['region'],
                 'properties': {
                     'region': {
                         'default': None,
                         'type': 'string',
                         'description': 'Region to generate inventory for'},
                     'cell': {
                         'default': None,
                         'type': 'string',
                         'description': 'Cell to generate inventory for'}}}
    },
    ('hosts_id_data', 'PUT'): {'json': DefinitionsData},
    ('hosts_id', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'resolved-values': {
                         'default': True,
                         'type': 'boolean'}}}
    },
    ('hosts_id', 'PUT'): {'json': DefinitionsHost},
    ('regions', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the region to get'},
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'ID of the region to get'}}}
        },
    ('regions', 'POST'): {'json': DefinitionsRegion},
    ('regions_id_data', 'PUT'): {'json': DefinitionsData},
    ('hosts', 'POST'): {'json': DefinitionsHost},
    ('hosts', 'GET'): {
        'args': {'required': ['region'],
                 'properties': {
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the hosts to get'},
                     'region': {
                         'default': None,
                         'type': 'integer',
                         'description': 'ID of the region to get hosts'},
                     'cell': {
                         'default': None,
                         'type': 'integer',
                         'description': 'ID of the cell to get hosts'},
                     'device_type': {
                         'default': None,
                         'type': 'string',
                         'description': 'Type of host to get'},
                     'limit': {
                         'minimum': 1,
                         'description': 'number of hosts to return',
                         'default': 1000,
                         'type': 'integer',
                         'maximum': 10000},
                     'ip': {
                         'default': None,
                         'type': 'string',
                         'description': 'ip_address of the hosts to get'},
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'ID of host to get'}}
                 }},
    ('cells_id', 'PUT'): {'json': DefinitionsCell},
    ('cells', 'POST'): {'json': DefinitionsCell},
    ('cells', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'region': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the region to get cells for'},
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'id of the cell to get'
                         },
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the cell to get'}}
                 }},
    ('regions_id', 'PUT'): {'json': DefinitionsRegion},
    ('cells_id_data', 'PUT'): {'json': DefinitionsData},
    ('projects', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'id of the project to get'
                         },
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the project to get'}}
                 }},
    ('projects', 'POST'): {'json': DefinitionProject},
    ('users', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'id of the user to get'
                         },
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the user to get'}}
                 }},
    ('users', 'POST'): {'json': DefinitionUser},
    ('netdevices', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'id of the net device to get'
                         },
                     'ip': {
                         'default': None,
                         'type': 'string',
                         'description': 'IP of the device to get'},
                     'region_id': {
                         'default': None,
                         'type': 'string',
                         'description': 'region id of the device to get'},
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the device to get'},
                     'device_type': {
                         'default': None,
                         'type': 'string',
                         'description': 'type of the device to get'},
                     'cell_id': {
                         'default': None,
                         'type': 'string',
                         'description': 'cell id of the device to get'}}
                 }},
    ('netdevices_id', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'resolved-values': {
                         'default': True,
                         'type': 'boolean'}}}},
    ('netdevices', 'POST'): {'json': DefinitionNetDevice},
    ('net_interfaces', 'GET'): {
        'args': {'required': ['device_id'],
                 'properties': {
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'id of the net interface to get'
                         },
                     'device_id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'device id of the interface to get'},
                     'ip': {
                         'default': None,
                         'type': 'string',
                         'description': 'IP of the interface to get'},
                     'interface_type': {
                         'default': None,
                         'type': 'string',
                         'description': 'Type of the interface  to get'}}
                 }},
    ('net_interfaces', 'POST'): {'json': DefinitionNetInterface},
    ('networks', 'GET'): {
        'args': {'required': [],
                 'properties': {
                     'id': {
                         'default': None,
                         'type': 'integer',
                         'description': 'id of the network to get'
                         },
                     'network_type': {
                         'default': None,
                         'type': 'string',
                         'description': 'type of the network to get'},
                     'name': {
                         'default': None,
                         'type': 'string',
                         'description': 'name of the network to get'},
                     'region_id': {
                         'default': None,
                         'type': 'string',
                         'description': 'region id of the network to get'},
                     'cell_id': {
                         'default': None,
                         'type': 'string',
                         'description': 'cell idof the network to get'}}
                 }},
    ('networks', 'POST'): {'json': DefinitionNetwork},
}

filters = {
    ('hosts_id_data', 'PUT'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('hosts_id_data', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('hosts_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionsHostId},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('hosts_id', 'PUT'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('hosts_id', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('hosts', 'POST'):
        {200: {'headers': None, 'schema': DefinitionsHost},
         400: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('hosts', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionsHost, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionsCellId},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells_id', 'PUT'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells_id', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells_id_data', 'PUT'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells_id_data', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells', 'POST'):
        {200: {'headers': None, 'schema': DefinitionsCell},
         400: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('cells', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionsCell, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions', 'POST'):
        {200: {'headers': None, 'schema': DefinitionsRegion},
         400: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionsRegion, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions_id_data', 'PUT'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions_id_data', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionsRegionId},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions_id', 'PUT'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('regions_id', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('projects', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionProject, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('projects', 'POST'):
        {200: {'headers': None, 'schema': DefinitionProject},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('users', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionUser, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('users', 'POST'):
        {200: {'headers': None, 'schema': DefinitionUser},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('users_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionUser},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('users_id', 'DELETE'):
        {200: {'headers': None, 'schema': None},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('netdevices', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionNetDeviceId, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('netdevices_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionNetDeviceId},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('networks', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionNetwork, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('networks_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionNetworkId},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('net_interfaces', 'GET'):
        {200: {'headers': None,
               'schema': {'items': DefinitionNetInterface, 'type': 'array'}},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
    ('net_interfaces_id', 'GET'):
        {200: {'headers': None, 'schema': DefinitionNetInterfaceId},
         400: {'headers': None, 'schema': None},
         404: {'headers': None, 'schema': None},
         405: {'headers': None, 'schema': None}},
}


scopes = {
    ('hosts_id_data', 'PUT'): [],
    ('hosts_id_data', 'DELETE'): [],
    ('hosts_id', 'PUT'): [],
    ('hosts_id', 'DELETE'): [],
    ('regions', 'GET'): [],
    ('regions_id_data', 'PUT'): [],
    ('regions_id_data', 'DELETE'): [],
    ('hosts', 'POST'): [],
    ('hosts', 'GET'): [],
    ('cells_id', 'PUT'): [],
    ('cells_id', 'DELETE'): [],
    ('cells', 'POST'): [],
    ('cells', 'GET'): [],
    ('regions_id', 'PUT'): [],
    ('cells_id_data', 'PUT'): [],
    ('cells_id_data', 'DELETE'): [],
    ('projects', 'GET'): [],
    ('projects_id', 'GET'): [],
    ('projects_id', 'DELETE'): [],
    ('projects', 'POST'): [],
    ('users', 'GET'): [],
    ('users', 'POST'): [],
    ('users_id', 'GET'): [],

}


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    return normalize(schema, value, type_defaults)[0]


def normalize(schema, data, required_defaults=None):

    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            if hasattr(self.data, key):
                return getattr(self.data, key)
            else:
                return default

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return self.data.keys()
            return vars(self.data).keys()

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')
            if ('default' not in _schema and
                key in schema.get('required', []) and
                    type_ in required_defaults):
                _schema['default'] = required_defaults[type_]

            # get value
            if data.has(key):
                result[key] = _normalize(_schema, data.get(key))
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                errors.append(dict(name='property_missing',
                                   message='`%s` is required' % key))

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            rs_component.update(result)
            result = rs_component

        additional_properties_schema = schema.get('additionalProperties',
                                                  False)
        if additional_properties_schema:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema,
                                         data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, dict):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize(schema, data):
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if type_ not in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors
