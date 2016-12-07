import copy


"""
Provides some fake resources - region, cell, host and other related
objects for test.
"""


class Project(object):
    def __init__(self, name):
        self.name = name

    def items(self):
        return iter(self.__dict__.items())


PROJECT1 = Project("project1")
PROJECT2 = Project("project2")


class User(object):
    def __init__(self, username, project_id, is_admin, is_root,
                 api_key, roles=None):
        self.username = username
        self.project_id = project_id
        self.is_admin = is_admin
        self.is_root = is_root
        self.api_key = api_key
        self.roles = roles

    def items(self):
        return iter(self.__dict__.items())


USER1 = User('user1', "2757a1b4-cd90-4891-886c-a246fd4e7064", True, False,
             'xx-yy-zz')
USER2 = User('user2', "05d081ca-dcf5-4e96-b132-23b94d665799", False, False,
             'aa-bb-cc')


class Cell(object):
    def __init__(self, name, status, region_id, project_id, variables,
                 labels=None):
        self.name = name
        self.status = status
        self.region_id = region_id
        self.project_id = project_id
        self.variables = variables
        self.labels = labels

    def items(self):
        return iter(self.__dict__.items())


CELL1 = Cell("cell1", "active", 1, 1, {"key1": "value1",
                                       "key2": "value2"})
CELL2 = Cell("cell2", "active", "2", "abcd", {"key3": "value3",
                                              "key4": "value4"})
CELL3 = Cell("cell1", "active", 2, 1, {"key1": "value1",
                                       "key2": "value2"})

CELL_LIST = [CELL1, CELL2]
CELL_LIST2 = [CELL1, CELL3]


class Region(object):
    def __init__(self, name, project_id, variables, labels=None):
        self.name = name
        self.project_id = project_id
        self.variables = variables
        self.labels = labels

    def items(self):
        return iter(self.__dict__.items())


REGION1 = Region("region1", "abcd", {"key1": "value1", "key2": "value2"})
REGION2 = Region("region2", "abcd", {"key3": "value3", "key4": "value4"})
REGIONS_LIST = [REGION1, REGION2]


class Host(object):
    def __init__(self, name, project_id, region_id, ip_address,
                 device_type, variables, labels=None):
        self.name = name
        self.project_id = project_id
        self.region_id = region_id
        self.ip_address = ip_address
        self.variables = variables
        self.resolved = copy.copy(variables)
        self.device_type = device_type
        self.labels = labels

    def items(self):
        return iter(self.__dict__.items())


HOST1 = Host("www.craton.com", 1, 1, "192.168.1.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST2 = Host("www.example.com", "1", "1", "192.168.1.2", "server",
             {"key1": "value1", "key2": "value2"})
HOST3 = Host("www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST4 = Host("www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"}, labels=["a", "b"])
HOSTS_LIST_R1 = [HOST1, HOST2]
HOSTS_LIST_R2 = [HOST3]
HOSTS_LIST_R3 = [HOST1, HOST2, HOST3]


class Networks(object):
    def __init__(self, name, project_id, cidr, gateway, netmask,
                 variables, region_id, labels=None):
        self.name = name
        self.project_id = project_id
        self.cidr = cidr
        self.gateway = gateway
        self.netmask = netmask
        self.variables = variables
        self.labels = labels
        self.region_id = region_id

    def items(self):
        return iter(self.__dict__.items())


NETWORK1 = Networks("PrivateNetwork", 1, "192.168.1.0/24", "192.168.1.1",
                    "255.255.255.0", {"key1": "value1"}, 1)
NETWORK2 = Networks("PublicNetwork", 1, "10.10.1.0/24", "10.10.1.1",
                    "255.255.255.0", {"pkey1": "pvalue1"}, 1)
NETWORK3 = Networks("OtherNetwork", 1, "10.10.1.0/24", "10.10.1.2",
                    "255.255.255.0", {"okey1": "ovalue1"}, 2)
NETWORKS_LIST = [NETWORK1, NETWORK2]
NETWORKS_LIST2 = [NETWORK1, NETWORK2, NETWORK3]


class NetworkDevice():
    def __init__(self, region_id, ip_address):
        self.region_id = region_id
        self.ip_address = ip_address

    def items(self):
        return iter(self.__dict__.items())


NETWORK_DEVICE1 = NetworkDevice(1, '10.10.0.1')
NETWORK_DEVICE2 = NetworkDevice(2, '10.10.0.2')

NETWORK_DEVICE_LIST1 = [NETWORK_DEVICE1]
NETWORK_DEVICE_LIST2 = [NETWORK_DEVICE1, NETWORK_DEVICE2]


class NetworkInterface():
    def __init__(self, name, device_id, interface_type, ip_address):
        self.name = name
        self.device_id = device_id
        self.interface_type = interface_type
        self.ip_address = ip_address

    def items(self):
        return iter(self.__dict__.items())


NETWORK_INTERFACE1 = NetworkInterface(
    'NetworkDevice1', 1, 'interface_type1', '10.10.0.1'
)
NETWORK_INTERFACE2 = NetworkInterface(
    'NetworkDevice2', 2, 'interface_type2', '10.10.0.2'
)
NETWORK_INTERFACE_LIST1 = [NETWORK_INTERFACE1]
NETWORK_INTERFACE_LIST2 = [NETWORK_INTERFACE1, NETWORK_INTERFACE2]
