DefinitionVariablesSource = {
    "type": "object",
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

DefinitionsHost = {
    "required": [
        "name",
        "region_id",
        "ip_address",
        "device_type",
    ],
    "type": "object",
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
        "id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
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
    },
}

DefinitionsHostId = {
    "type": "object",
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
        "id": {
            "type": "integer",
        },
        "cell_id": {
            "type": "integer",
        },
        "project_id": {
            "type": "string",
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
    },
}

DefinitionsCell = {
    "required": [
        "name",
        "region_id",
    ],
    "type": "object",
    "properties": {
        "note": {
            "type": "string",
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

DefinitionsCellId = {
    "type": "object",
    "properties": {
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
    "properties": {
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
        "id": {
            "type": "integer",
            "description": "Unique ID for the region",
        },
        "variables": DefinitionVariablesSource,
    },
}

DefinitionsRegionId = {
    "type": "object",
    "properties": {
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
    "properties": {
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
    "properties": {
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
    "properties": {
        "id": {
            "type": "integer",
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

DefinitionNetworkId = {
    "type": "object",
    "properties": {
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
    "properties": {
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
    "properties": {
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
        "hostname",
        "region_id",
        "device_type",
        "ip_address",
    ],
    "type": "object",
    "properties": {
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
        "ip_address": {
            "type": "string",
        },
        "device_type": {
            "type": "string",
        },
        "hostname": {
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
    "properties": {
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
        "ip_address": {
            "type": "string",
        },
        "device_type": {
            "type": "string",
        },
        "hostname": {
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

validators = {
    ("ansible_inventory", "GET"): {
        "args": {
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
    ("hosts_id_variables", "PUT"): {
        "json": DefinitionVariablesSource,
    },
    ("hosts_id_variables", "DELETE"): {
        "json": DefinitionVariablesSource,
    },
    ("hosts_labels", "PUT"): {
        "json": DefinitionsLabel,
    },
    ("hosts_labels", "GET"): {
    },
    ("hosts_labels", "DELETE"): {
        "json": DefinitionsLabel,
    },
    ("hosts_id", "DELETE"): {
    },
    ("hosts_id", "GET"): {
        "args": {
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
            },
        },
    },
    ("hosts_id_variables", "GET"): {
        "args": {
            "properties": {
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            },
        },
    },
    ("regions", "GET"): {
        "args": {
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
            },
        },
    },
    ("regions", "POST"): {
        "json": DefinitionsRegion,
    },
    ("regions_id_variables", "PUT"): {
        "json": DefinitionVariablesSource,
    },
    ("regions_id_variables", "GET"): {
    },
    ("regions_id_variables", "DELETE"): {
        "json": DefinitionVariablesSource,
    },
    ("hosts", "POST"): {
        "json": DefinitionsHost,
    },
    ("hosts", "GET"): {
        "args": {
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
                "limit": {
                    "minimum": 1,
                    "description": "number of hosts to return",
                    "default": 1000,
                    "type": "integer",
                    "maximum": 10000,
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
            },
        },
    },
    ("cells_id", "DELETE"): {
    },
    ("cells_id", "GET"): {
    },
    ("cells_id", "PUT"): {
        "json": {
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
            },
        },
    },
    ("regions_id", "DELETE"): {
    },
    ("regions_id", "GET"): {
    },
    ("regions_id", "PUT"): {
        "json": {
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
    ("cells_id_variables", "PUT"): {
        "json": DefinitionVariablesSource,
    },
    ("cells_id_variables", "GET"): {
    },
    ("cells_id_variables", "DELETE"): {
        "json": DefinitionVariablesSource,
    },
    ("projects", "GET"): {
        "args": {
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
            },
        },
    },
    ("projects", "POST"): {
        "json": DefinitionProject,
    },
    ("projects_id", "DELETE"): {
    },
    ("projects_id", "GET"): {
    },
    ("users", "GET"): {
        "args": {
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
            },
        },
    },
    ("users", "POST"): {
        "json": DefinitionUser,
    },
    ("users_id", "DELETE"): {
    },
    ("users_id", "GET"): {
    },
    ("network_devices", "GET"): {
        "args": {
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
            },
        },
    },
    ("network_devices_id", "DELETE"): {
    },
    ("network_devices_id", "GET"): {
        "args": {
            "properties": {
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            },
        },
    },
    ("network_devices_id_variables", "PUT"): {
        "json": DefinitionVariablesSource
    },
    ("network_devices_id_variables", "GET"): {
    },
    ("network_devices_id_variables", "DELETE"): {
        "json": DefinitionVariablesSource
    },
    ("networks_id", "DELETE"): {
    },
    ("networks_id", "GET"): {
    },
    ("networks_id", "PUT"): {
        "json": {
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
            "properties": {
                "ip_address": {
                    "type": "string",
                },
                "device_type": {
                    "type": "string",
                },
                "hostname": {
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
    },
    ("network_devices_labels", "PUT"): {
        "json": DefinitionsLabel,
    },
    ("network_interfaces", "GET"): {
        "args": {
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
            },
        },
    },
    ("network_interfaces", "POST"): {
        "json": DefinitionNetworkInterface,
    },
    ("network_interfaces_id", "DELETE"): {
    },
    ("network_interfaces_id", "GET"): {
    },
    ("network_interfaces_id", "PUT"): {
        "json": {
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
            },
        },
    },
    ("networks_id_variables", "PUT"): {
        "json": DefinitionVariablesSource
    },
    ("networks_id_variables", "GET"): {
    },
    ("networks_id_variables", "DELETE"): {
        "json": DefinitionVariablesSource
    },
    ("networks", "POST"): {
        "json": DefinitionNetwork,
    },
}

filters = {
    ("hosts_id_variables", "PUT"): {
        200: {
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
    ("hosts_id_variables", "DELETE"): {
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
        200: {
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
            "schema": {
                "items": DefinitionsHost,
                "type": "array",
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
    ("cells_id_variables", "PUT"): {
        200: {
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
    ("cells_id_variables", "DELETE"): {
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
        200: {
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
            "schema": {
                "items": DefinitionsCell,
                "type": "array",
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
    ("regions", "POST"): {
        200: {
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
            "schema": {
                "items": DefinitionsRegion,
                "type": "array",
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
    ("regions_id_variables", "PUT"): {
        200: {
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
    ("regions_id_variables", "DELETE"): {
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
            "schema": {
                "items": DefinitionProject,
                "type": "array",
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
    ("projects", "POST"): {
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
    ("users", "GET"): {
        200: {
            "headers": None,
            "schema": {
                "items": DefinitionUser,
                "type": "array",
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
    ("users", "POST"): {
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
            "schema": {
                "items": DefinitionNetworkDeviceId,
                "type": "array",
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
    ("network_devices_id_variables", "PUT"): {
        200: {
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
    ("network_devices_id_variables", "DELETE"): {
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
    ("networks", "GET"): {
        200: {
            "headers": None,
            "schema": {
                "items": DefinitionNetwork,
                "type": "array",
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
    ("networks_id_variables", "PUT"): {
        200: {
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
    ("networks_id_variables", "DELETE"): {
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
    ("network_interfaces", "GET"): {
        200: {
            "headers": None,
            "schema": {
                "items": DefinitionNetworkInterface,
                "type": "array",
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
}

scopes = {
    ("hosts_id_variables", "PUT"): [],
    ("hosts_id_variables", "DELETE"): [],
    ("hosts_id", "PUT"): [],
    ("hosts_id", "DELETE"): [],
    ("regions", "GET"): [],
    ("regions_id_variables", "PUT"): [],
    ("regions_id_variables", "DELETE"): [],
    ("hosts", "POST"): [],
    ("hosts", "GET"): [],
    ("cells_id", "PUT"): [],
    ("cells_id", "DELETE"): [],
    ("cells", "POST"): [],
    ("cells", "GET"): [],
    ("regions_id", "PUT"): [],
    ("cells_id_variables", "PUT"): [],
    ("cells_id_variables", "DELETE"): [],
    ("projects", "GET"): [],
    ("projects_id", "GET"): [],
    ("projects_id", "DELETE"): [],
    ("projects", "POST"): [],
    ("users", "GET"): [],
    ("users", "POST"): [],
    ("users_id", "GET"): [],
    ("network_devices_id_variables", "PUT"): [],
    ("network_devices_id_variables", "DELETE"): [],
    ("networks_id_variables", "PUT"): [],
    ("networks_id_variables", "DELETE"): [],
}
