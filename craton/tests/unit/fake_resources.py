"""
Provides some fake resources - region, cell, host and other related
objects for test.
"""


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
        self.resolved = variables
        self.device_type = device_type
        self.labels = labels

HOST1 = Host("www.craton.com", "1", "1", "192.168.1.1", "server",
             {"key1": "value1", "key2": "value2"})
HOST2 = Host("www.example.com", "1", "1", "192.168.1.2", "server",
             {"key1": "value1", "key2": "value2"})
HOST3 = Host("www.example.net", "1", "2", "10.10.0.1", "server",
             {"key1": "value1", "key2": "value2"})
HOSTS_LIST_R1 = [HOST1, HOST2]
HOSTS_LIST_R2 = [HOST3]
