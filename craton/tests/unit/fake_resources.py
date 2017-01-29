import copy


"""
Provides some fake resources - region, cell, host and other related
objects for test.
"""


class Project(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def items(self):
        return iter(self.__dict__.items())


PROJECT1 = Project(1, "project1")
PROJECT2 = Project(2, "project2")


class User(object):
    def __init__(self, id, username, project_id, is_admin, is_root,
                 api_key, roles=None):
        self.id = id
        self.username = username
        self.project_id = project_id
        self.is_admin = is_admin
        self.is_root = is_root
        self.api_key = api_key
        self.roles = roles

    def items(self):
        return iter(self.__dict__.items())


USER1 = User(1, 'user1', "2757a1b4-cd90-4891-886c-a246fd4e7064", True, False,
             'xx-yy-zz')
USER2 = User(2, 'user2', "05d081ca-dcf5-4e96-b132-23b94d665799", False, False,
             'aa-bb-cc')


class Cell(object):
    def __init__(self, id, name, status, region_id, project_id, variables,
                 labels=None):
        self.id = id
        self.name = name
        self.status = status
        self.region_id = region_id
        self.project_id = project_id
        self.variables = variables
        self.labels = labels

    def items(self):
        return iter(self.__dict__.items())


CELL1 = Cell(1, "cell1", "active", 1, 1, {"key1": "value1",
                                          "key2": "value2"})
CELL2 = Cell(2, "cell2", "active", "2", "abcd", {"key3": "value3",
                                                 "key4": "value4"})
CELL3 = Cell(3, "cell1", "active", 2, 1, {"key1": "value1",
                                          "key2": "value2"})

CELL_LIST = [CELL1, CELL2]
CELL_LIST2 = [CELL1, CELL3]


class Region(object):
    def __init__(self, id, name, project_id, variables, labels=None):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.variables = variables
        self.labels = labels

    def items(self):
        return iter(self.__dict__.items())


REGION1 = Region(1, "region1", "abcd", {"key1": "value1", "key2": "value2"})
REGION2 = Region(2, "region2", "abcd", {"key3": "value3", "key4": "value4"})
REGIONS_LIST = [REGION1, REGION2]


class Host(object):
    def __init__(self, id, name, project_id, region_id, ip_address,
                 device_type, variables, labels=None):
        self.id = id
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


HOST1 = Host(1, "www.craton.com", 1, 1, "192.168.1.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST2 = Host(2, "www.example.com", "1", "1", "192.168.1.2", "server",
             {"key1": "value1", "key2": "value2"})
HOST3 = Host(3, "www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST4 = Host(4, "www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"}, labels=["a", "b"])
HOSTS_LIST_R1 = [HOST1, HOST2]
HOSTS_LIST_R2 = [HOST3]
HOSTS_LIST_R3 = [HOST1, HOST2, HOST3]


class Networks(object):
    def __init__(self, id, name, project_id, cidr, gateway, netmask,
                 variables, region_id, labels=None):
        self.id = id
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


NETWORK1 = Networks(1, "PrivateNetwork", 1, "192.168.1.0/24", "192.168.1.1",
                    "255.255.255.0", {"key1": "value1"}, 1)
NETWORK2 = Networks(2, "PublicNetwork", 1, "10.10.1.0/24", "10.10.1.1",
                    "255.255.255.0", {"pkey1": "pvalue1"}, 1)
NETWORK3 = Networks(3, "OtherNetwork", 1, "10.10.1.0/24", "10.10.1.2",
                    "255.255.255.0", {"okey1": "ovalue1"}, 2)
NETWORKS_LIST = [NETWORK1, NETWORK2]
NETWORKS_LIST2 = [NETWORK1, NETWORK2, NETWORK3]


class NetworkDevice():
    def __init__(self, id, hostname, project_id, region_id,
                 device_type, ip_address, variables, labels=None):
        self.id = id
        self.hostname = hostname
        self.project_id = project_id
        self.region_id = region_id
        self.device_type = device_type
        self.ip_address = ip_address
        self.variables = variables
        self.resolved = copy.copy(variables)
        self.labels = labels

    def items(self):
        return iter(self.__dict__.items())


NETWORK_DEVICE1 = NetworkDevice(1, "NetDevices1", 1, 1, "Server", "10.10.0.1",
                                {"key1": "value1", "key2": "value2"},
                                labels=["a", "b"])
NETWORK_DEVICE2 = NetworkDevice(2, "NetDevices2", 1, 2, "Server", "10.10.0.2",
                                {"key1": "value1", "key2": "value2"},
                                labels=["a", "b"])

NETWORK_DEVICE_LIST1 = [NETWORK_DEVICE1]
NETWORK_DEVICE_LIST2 = [NETWORK_DEVICE1, NETWORK_DEVICE2]


class NetworkInterface():
    def __init__(self, id, name, device_id, project_id, interface_type,
                 ip_address, variables):
        self.id = id
        self.name = name
        self.device_id = device_id
        self.project_id = project_id
        self.interface_type = interface_type
        self.ip_address = ip_address
        self.variables = variables

    def items(self):
        return iter(self.__dict__.items())


NETWORK_INTERFACE1 = NetworkInterface(1, "NetInterface", 1, 1,
                                      "interface_type1", "10.10.0.1",
                                      {"key1": "value1", "key2": "value2"})
NETWORK_INTERFACE2 = NetworkInterface(2, "NetInterface", 2, 1,
                                      "interface_type2", "10.10.0.2",
                                      {"key1": "value1", "key2": "value2"})

NETWORK_INTERFACE_LIST1 = [NETWORK_INTERFACE1]
NETWORK_INTERFACE_LIST2 = [NETWORK_INTERFACE1, NETWORK_INTERFACE2]
