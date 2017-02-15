DefinitionVariablesSource = {
    "type": "object",
    "additionalProperties": False,
    "patternProperties": {
        "^.+": {
            "anyOf": [
                {
                    "type": "string",
                },
                {
                    "type": "null",
                },
                {
                    "type": "number",
                },
                {
                    "type": "boolean",
                },
                {
                    "type": "integer",
                },
                {
                    "type": "array",
                },
                {
                    "type": "object",
                },
            ],
        },
    },
}

DefinitionDeleteVariables = {
    "type": "array",
    "items": {"type": "string"},
}

DefinitionLinks = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "href",
            "rel",
        ],
        "properties": {
            "href": {
                "type": "string",
            },
            "rel": {
                "type": "string",
            }
        }
    }
}

DefinitionsHost = {
    "required": [
        "name",
        "region_id",
        "ip_address",
        "device_type",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "active": {
            "type": "boolean",
        },
        "note": {
            "type": "string",
        },
        "ip_address": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "parent_id": {
            "type": "integer",
            "description": "Parent Id of this host",
        },
        "device_type": {
            "type": "string",
            "description": "Type of host",
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
            },
            "description": "User defined labels",
        },
        "region_id": {
            "type": "integer",
        },
        "variables": DefinitionVariablesSource,
        "links": DefinitionLinks,
    },
}

DefinitionsHostId = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "active": {
            "type": "boolean",
        },
        "note": {
            "type": "string",
        },
        "ip_address": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "parent_id": {
            "type": "integer",
            "description": "Parent Id of this host",
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
            },
            "description": "User defined labels",
        },
        "device_type": {
            "type": "string",
            "description": "Type of host",
        },
        "region_id": {
            "type": "integer",
        },
        "variables": DefinitionVariablesSource,
        "links": DefinitionLinks,
    },
}

DefinitionsCell = {
    "required": [
        "name",
        "region_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "note": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "region_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "id": {
            "type": "integer",
            "description": "Unique ID of the cell",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionsCellId = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "note": {
            "type": "string",
        },
        "project_id": {
            "type": "string",
            "description": "UUID of the project",
        },
        "name": {
            "type": "string",
        },
        "region_id": {
            "type": "integer",
        },
        "id": {
            "type": "integer",
            "description": "Unique ID of the cell",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionsLabel = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },
}

DefinitionsError = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "fields": {
            "type": "string",
        },
        "message": {
            "type": "string",
        },
        "code": {
            "type": "integer",
            "format": "int32",
        },
    },
}

DefinitionsRegion = {
    "required": [
        "name",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "note": {
            "type": "string",
            "description": "Region Note",
        },
        "name": {
            "type": "string",
            "description": "Region Name",
        },
        "cells": {
            "items": DefinitionsCell,
            "type": "array",
            "description": "List of cells in this region",
        },
        "project_id": {
            "type": "string",
        },
        "id": {
            "type": "integer",
            "description": "Unique ID for the region",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionsRegionId = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "note": {
            "type": "string",
            "description": "Region Note",
        },
        "name": {
            "type": "string",
            "description": "Region Name.",
        },
        "project_id": {
            "type": "string",
            "description": "UUID of the project",
        },
        "cells": {
            "items": DefinitionsCell,
            "type": "array",
            "description": "List of cells in this region",
        },
        "id": {
            "type": "integer",
            "description": "Unique ID for the region",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionUser = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "api_key": {
            "type": "string",
        },
        "username": {
            "type": "string",
        },
        "is_admin": {
            "type": "boolean",
        },
        "project_id": {
            "type": "string",
        },
        "roles": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },
}

DefinitionProject = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "name": {
            "type": "string",
        },
    },
}

DefinitionNetwork = {
    "required": [
        "name",
        "cidr",
        "gateway",
        "netmask",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "region_id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "cidr": {
            "type": "string",
        },
        "gateway": {
            "type": "string",
        },
        "netmask": {
            "type": "string",
        },
        "ip_block_type": {
            "type": "string",
        },
        "nss": {
            "type": "string",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionNetworkId = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "region_id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "name": {
            "type": "string",
        },
        "cidr": {
            "type": "string",
        },
        "gateway": {
            "type": "string",
        },
        "netmask": {
            "type": "string",
        },
        "ip_block_type": {
            "type": "string",
        },
        "nss": {
            "type": "string",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionNetworkInterface = {
    "required": [
        "name",
        "device_id",
        "interface_type",
        "ip_address",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "name": {
            "type": "string",
        },
        "device_id": {
            "type": "integer",
            "default": None,
        },
        "network_id": {
            "type": "integer",
            "default": None,
        },
        "interface_type": {
            "type": "string",
        },
        "project_id": {
            "type": "string",
        },
        "vlan_id": {
            "type": "integer",
        },
        "vlan": {
            "type": "string",
        },
        "port": {
            "type": "integer",
        },
        "duplex": {
            "type": "string",
        },
        "speed": {
            "type": "integer",
        },
        "link": {
            "type": "string",
        },
        "cdp": {
            "type": "string",
        },
        "security": {
            "type": "string",
        },
        "ip_address": {
            "type": "string",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionNetworkInterfaceId = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "name": {
            "type": "string",
        },
        "device_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "network_id": {
            "type": "integer",
        },
        "interface_type": {
            "type": "string",
        },
        "vlan_id": {
            "type": "integer",
        },
        "vlan": {
            "type": "string",
        },
        "port": {
            "type": "string",
        },
        "duplex": {
            "type": "string",
        },
        "speed": {
            "type": "integer",
        },
        "link": {
            "type": "string",
        },
        "cdp": {
            "type": "string",
        },
        "security": {
            "type": "string",
        },
        "ip_address": {
            "type": "string",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionNetworkDevice = {
    "required": [
        "name",
        "region_id",
        "device_type",
        "ip_address",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "region_id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "parent_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "ip_address": {
            "type": "string",
        },
        "device_type": {
            "type": "string",
        },
        "active": {
            "type": "boolean",
        },
        "name": {
            "type": "string",
        },
        "access_secret_id": {
            "type": "integer",
        },
        "model_name": {
            "type": "string",
        },
        "os_version": {
            "type": "string",
        },
        "vlans": {
            "type": "string",
        },
        "interface_id": {
            "type": "integer",
        },
        "network_id": {
            "type": "integer",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionNetworkDeviceId = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "created_at": {
            "type": "string",
        },
        "updated_at": {
            "type": "string",
        },
        "id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
        },
        "region_id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "parent_id": {
            "type": "integer",
        },
        "active": {
            "type": "boolean",
        },
        "ip_address": {
            "type": "string",
        },
        "device_type": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "access_secret_id": {
            "type": "integer",
        },
        "model_name": {
            "type": "string",
        },
        "os_version": {
            "type": "string",
        },
        "vlans": {
            "type": "string",
        },
        "interface_id": {
            "type": "integer",
        },
        "network_id": {
            "type": "integer",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionNoParams = {
    "type": "object",
    "properties": {},
    "maxProperties": 0,
    "additionalProperties": False,
}

DefinitionsPaginationLinks = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "rel": {
                "type": "string",
                "enum": ["first", "prev", "self", "next"],
                "description": ("Relation of the associated URL to the current"
                                " page"),
            },
            "href": {
                "type": "string",
            },
        },
    },
}


def paginated_resource(list_name, schema):
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            list_name: {
                "type": "array",
                "items": schema,
            },
            "links": DefinitionsPaginationLinks,
        },
    }

validators = {
    ("ansible_inventory", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "region_id": {
                    "default": None,
                    "type": "string",
                    "description": "Region to generate inventory for",
                },
                "cell_id": {
                    "default": None,
                    "type": "string",
                    "description": "Cell id to generate inventory for",
                },
            },
        },
    },
    ("hosts_labels", "PUT"): {
        "json": DefinitionsLabel,
    },
    ("hosts_labels", "GET"): {
        "args": DefinitionNoParams,
    },
    ("hosts_labels", "DELETE"): {
        "json": DefinitionsLabel,
    },
    ("hosts_id", "DELETE"): {
    },
    ("hosts_id", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            },
        },
    },
    ("hosts_id", "PUT"): {
        "json": {
            "additionalProperties": False,
            "properties": {
                "active": {
                    "type": "boolean",
                },
                "note": {
                    "type": "string",
                },
                "ip_address": {
                    "type": "string",
                },
                "name": {
                    "type": "string",
                },
                "device_type": {
                    "type": "string",
                    "description": "Type of host",
                },
                "parent_id": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Parent Id of this host",
                },
            },
        },
    },
    ("regions", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "description": "name of the region to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a region",
                },
                "id": {
                    "type": "integer",
                    "description": "ID of the region to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of regions to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last region ID of the previous page",
                },
            },
        },
    },
    ("regions", "POST"): {
        "json": DefinitionsRegion,
    },
    ("hosts", "POST"): {
        "json": DefinitionsHost,
    },
    ("hosts", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "description": "name of the hosts to get",
                },
                "region_id": {
                    "type": "integer",
                    "description": "ID of the region to get hosts",
                },
                "cell_id": {
                    "type": "integer",
                    "description": "ID of the cell to get hosts",
                },
                "device_type": {
                    "type": "string",
                    "description": "Type of host to get",
                },
                "label": {
                    "type": "string",
                    "description": "label to get host by",
                },
                "ip_address": {
                    "type": "string",
                    "description": "ip_address of the hosts to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a host",
                },
                "id": {
                    "type": "integer",
                    "description": "ID of host to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of hosts to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last host ID of the previous page",
                },
            },
        },
    },
    ("cells_id", "DELETE"): {
    },
    ("cells_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("cells_id", "PUT"): {
        "json": {
            "additionalProperties": False,
            "properties": {
                "note": {
                    "type": "string",
                },
                "name": {
                    "type": "string",
                },
            },
        },
    },
    ("cells", "POST"): {
        "json": DefinitionsCell,
    },
    ("cells", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "region_id": {
                    "type": "string",
                    "description": "name of the region to get cells for",
                },
                "id": {
                    "type": "integer",
                    "description": "id of the cell to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a cell",
                },
                "name": {
                    "type": "string",
                    "description": "name of the cell to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of cells to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last cell ID of the previous page",
                },
            },
        },
    },
    ("regions_id", "DELETE"): {
    },
    ("regions_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("regions_id", "PUT"): {
        "json": {
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                },
                "note": {
                    "type": "string",
                },
            },
        },
    },
    ("projects", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "id": {
                    "default": None,
                    "type": "integer",
                    "description": "id of the project to get",
                },
                "name": {
                    "default": None,
                    "type": "string",
                    "description": "name of the project to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of projects to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last project ID of the previous page",
                },
            },
        },
    },
    ("projects", "POST"): {
        "json": DefinitionProject,
    },
    ("projects_id", "DELETE"): {
    },
    ("projects_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("users", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "id": {
                    "default": None,
                    "type": "integer",
                    "description": "id of the user to get",
                },
                "name": {
                    "default": None,
                    "type": "string",
                    "description": "name of the user to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of users to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last user ID of the previous page",
                },
            },
        },
    },
    ("users", "POST"): {
        "json": DefinitionUser,
    },
    ("users_id", "DELETE"): {
    },
    ("users_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("network_devices", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "id of the net device to get",
                },
                "ip_address": {
                    "type": "string",
                    "description": "IP of the device to get",
                },
                "region_id": {
                    "type": "string",
                    "description": "region id of the device to get",
                },
                "name": {
                    "type": "string",
                    "description": "name of the device to get",
                },
                "device_type": {
                    "type": "string",
                    "description": "type of the device to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get device",
                },
                "cell_id": {
                    "type": "string",
                    "description": "cell id of the device to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of devices to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last device ID of the previous page",
                },
            },
        },
    },
    ("network_devices_id", "DELETE"): {
    },
    ("network_devices_id", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            },
        },
    },
    ("networks_id", "DELETE"): {
    },
    ("networks_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("networks_id", "PUT"): {
        "json": {
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                },
                "cidr": {
                    "type": "string",
                },
                "gateway": {
                    "type": "string",
                },
                "netmask": {
                    "type": "string",
                },
                "ip_block_type": {
                    "type": "string",
                },
                "nss": {
                    "type": "string",
                },
            },
        },
    },
    ("network_devices_id", "PUT"): {
        "json": {
            "additionalProperties": False,
            "properties": {
                "ip_address": {
                    "type": "string",
                },
                "device_type": {
                    "type": "string",
                },
                "name": {
                    "type": "string",
                },
                "model_name": {
                    "type": "string",
                },
                "os_version": {
                    "type": "string",
                },
                "vlans": {
                    "type": "string",
                },
                "parent_id": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                },
            },
        },
    },
    ("network_devices", "POST"): {
        "json": DefinitionNetworkDevice,
    },
    ("network_devices_labels", "DELETE"): {
        "json": DefinitionsLabel,
    },
    ("network_devices_labels", "GET"): {
        "args": DefinitionNoParams,
    },
    ("network_devices_labels", "PUT"): {
        "json": DefinitionsLabel,
    },
    ("network_interfaces", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "id of the net interface to get",
                },
                "device_id": {
                    "type": "integer",
                    "description": "device id of the interface to get",
                },
                "ip_address": {
                    "type": "string",
                    "description": "IP of the interface to get",
                },
                "interface_type": {
                    "type": "string",
                    "description": "Type of the interface  to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of interfaces to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last interface ID of the previous page",
                },
            },
        },
    },
    ("network_interfaces", "POST"): {
        "json": DefinitionNetworkInterface,
    },
    ("network_interfaces_id", "DELETE"): {
    },
    ("network_interfaces_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("network_interfaces_id", "PUT"): {
        "json": {
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                },
                "interface_type": {
                    "type": "string",
                },
                "vlan": {
                    "type": "string",
                },
                "port": {
                    "type": "string",
                },
                "duplex": {
                    "type": "string",
                },
                "speed": {
                    "type": "integer",
                },
                "link": {
                    "type": "string",
                },
                "cdp": {
                    "type": "string",
                },
                "security": {
                    "type": "string",
                },
            },
        },
    },
    ("networks", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "id of the network to get",
                },
                "network_type": {
                    "type": "string",
                    "description": "type of the network to get",
                },
                "name": {
                    "type": "string",
                    "description": "name of the network to get",
                },
                "region_id": {
                    "type": "string",
                    "description": "region id of the network to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get networks",
                },
                "cell_id": {
                    "type": "string",
                    "description": "cell idof the network to get",
                },
                "limit": {
                    "minimum": 10,
                    "default": 30,
                    "maximum": 100,
                    "type": "integer",
                    "description": "Number of networks to return in a page",
                },
                "marker": {
                    "type": "integer",
                    "description": "Last network ID of the previous page",
                },
            },
        },
    },
    ("networks", "POST"): {
        "json": DefinitionNetwork,
    },
    ("variables_with_resolve", "DELETE"): {
        "json": DefinitionDeleteVariables,
    },
    ("variables_with_resolve", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": {
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            },
        },
    },
    ("variables_with_resolve", "PUT"): {
        "json": DefinitionVariablesSource,
    },
    ("variables_without_resolve", "DELETE"): {
        "json": DefinitionDeleteVariables,
    },
    ("variables_without_resolve", "GET"): {
        "args": DefinitionNoParams,
    },
    ("variables_without_resolve", "PUT"): {
        "json": DefinitionVariablesSource,
    },
}

filters = {
    ("ansible_inventory", "GET"): {
        200: {
            "headers": None,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "patternProperties": {
                    "^.+": {
                        "anyOf": [
                            {
                                "type": "string",
                            },
                            {
                                "type": "null",
                            },
                            {
                                "type": "number",
                            },
                            {
                                "type": "boolean",
                            },
                            {
                                "type": "integer",
                            },
                            {
                                "type": "array",
                            },
                            {
                                "type": "object",
                            },
                        ],
                    },
                },
            },
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionsHostId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionsHostId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts_labels", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts_labels", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionsLabel,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts_labels", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionsLabel,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionsHost,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("hosts", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("hosts", DefinitionsHost),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("cells_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionsCellId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("cells_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionsCellId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("cells_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("cells", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionsCell,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("cells", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("cells", DefinitionsCell),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("regions", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionsRegion,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("regions", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("regions", DefinitionsRegion),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("regions_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionsRegionId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("regions_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionsRegionId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("regions_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("projects", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("projects", DefinitionProject),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("projects", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionProject,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("users", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("users", DefinitionUser),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("users", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionUser,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("projects_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionProject,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("projects_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("users_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionUser,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("users_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("network_devices",
                                         DefinitionNetworkDeviceId),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionNetworkDeviceId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionNetworkDeviceId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices_labels", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices_labels", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionsLabel,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices_labels", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionsLabel,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_devices_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionNetworkDeviceId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("networks", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("networks", DefinitionNetwork),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("networks", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionNetwork,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("networks_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("networks_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionNetworkId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("networks_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionNetworkId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_interfaces", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("network_interfaces",
                                         DefinitionNetworkInterface),
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_interfaces", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionNetworkInterface,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_interfaces_id", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_interfaces_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionNetworkInterfaceId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("network_interfaces_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionNetworkInterfaceId,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("variables_with_resolve", "GET"): {
        200: {
            "headers": None,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "variables": DefinitionVariablesSource,
                },
            },
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("variables_with_resolve", "PUT"): {
        200: {
            "headers": None,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "variables": DefinitionVariablesSource,
                },
            },
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("variables_with_resolve", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("variables_without_resolve", "DELETE"): {
        204: {
            "headers": None,
            "schema": None,
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("variables_without_resolve", "GET"): {
        200: {
            "headers": None,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "variables": DefinitionVariablesSource,
                },
            },
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
    ("variables_without_resolve", "PUT"): {
        200: {
            "headers": None,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "variables": DefinitionVariablesSource,
                },
            },
        },
        400: {
            "headers": None,
            "schema": None,
        },
        404: {
            "headers": None,
            "schema": None,
        },
        405: {
            "headers": None,
            "schema": None,
        },
    },
}
