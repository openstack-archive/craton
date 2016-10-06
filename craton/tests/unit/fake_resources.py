import copy


"""
Provides some fake resources - region, cell, host and other related
objects for test.
"""


class Label(object):
    def __init__(self, label):
        self.label = label

LABEL1 = Label("a")
LABEL2 = Label("b")
LABEL3 = Label("c")


class Project(object):
    def __init__(self, name):
        self.name = name

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

USER1 = User('user1', 1, True, False, 'xx-yy-zz')
USER2 = User('user2', 1, False, False, 'aa-bb-cc')


class Cell(object):
    def __init__(self, name, status, region_id, project_id, variables,
                 labels=None):
        self.name = name
        self.status = status
        self.region_id = region_id
        self.project_id = project_id
        self.variables = variables
        self.labels = labels

CELL1 = Cell("cell1", "active", "1", "abcd", {"key1": "value1",
                                              "key2": "value2"})
CELL2 = Cell("cell2", "active", "2", "abcd", {"key3": "value3",
                                              "key4": "value4"})

CELL_LIST = [CELL1, CELL2]


class Region(object):
    def __init__(self, name, project_id, variables, labels=None):
        self.name = name
        self.project_id = project_id
        self.variables = variables
        self.labels = labels

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

HOST1 = Host("www.craton.com", "1", "1", "192.168.1.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST2 = Host("www.example.com", "1", "1", "192.168.1.2", "server",
             {"key1": "value1", "key2": "value2"})
HOST3 = Host("www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST4 = Host("www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"}, labels=[LABEL1, LABEL2])
HOSTS_LIST_R1 = [HOST1, HOST2]
HOSTS_LIST_R2 = [HOST3]


class Networks(object):
    def __init__(self, name, project_id, cidr, gateway, netmask,
                 variables, labels=None):
        self.name = name
        self.project_id = project_id
        self.cidr = cidr
        self.gateway = gateway
        self.netmask = netmask
        self.variables = variables
        self.labels = labels

NETWORK1 = Networks("PrivateNetwork", 1, "192.168.1.0/24", "192.168.1.1",
                    "255.255.255.0", {"key1": "value1"})
NETWORK2 = Networks("PublicNetwork", 1, "10.10.1.0/24", "10.10.1.1",
                    "255.255.255.0", {"pkey1": "pvalue1"})
NETWORKS_LIST = [NETWORK1, NETWORK2]
