import copy

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

# These are properties that should be excluded in any POST call
# such that a resource can not be created with these in request body.
blacklisted_create_properties = ["id", "created_at", "updated_at"]


def _remove_properties(properties, remove_list):
    props = copy.copy(properties)
    for prop in remove_list:
        props.pop(prop)
    return props

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

HostProperties = {
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
    "cloud_id": {
        "type": "integer",
    },
    "variables": DefinitionVariablesSource,
    "links": DefinitionLinks,
}

DefinitionsHost = {
    "required": [
        "name",
        "cloud_id",
        "region_id",
        "ip_address",
        "device_type",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": HostProperties,
}

DefinitionsHostId = {
    "type": "object",
    "additionalProperties": False,
    "properties": HostProperties,
}

DefinitionHostCreate = {
    "required": [
        "name",
        "cloud_id",
        "region_id",
        "ip_address",
        "device_type",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(HostProperties,
                                     blacklisted_create_properties),
}

CellProperties = {
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
    "cloud_id": {
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
}

DefinitionsCell = {
    "required": [
        "name",
        "cloud_id",
        "region_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": CellProperties,
}

DefinitionsCellId = {
    "type": "object",
    "additionalProperties": False,
    "properties": CellProperties,
}

DefinitionsCellCreate = {
    "required": [
        "name",
        "cloud_id",
        "region_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(CellProperties,
                                     blacklisted_create_properties),
}

RegionProperties = {
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
    "cloud_id": {
        "type": "integer",
    },
    "id": {
        "type": "integer",
        "description": "Unique ID for the region",
    },
    "variables": DefinitionVariablesSource,
}

DefinitionsRegion = {
    "required": [
        "name",
        "cloud_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": RegionProperties,
}

DefinitionsRegionId = {
    "type": "object",
    "additionalProperties": False,
    "properties": RegionProperties,
}

DefinitionsRegionCreate = {
    "required": [
        "name",
        "cloud_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(RegionProperties,
                                     blacklisted_create_properties),
}

CloudProperties = {
    "created_at": {
        "type": "string",
    },
    "updated_at": {
        "type": "string",
    },
    "note": {
        "type": "string",
        "description": "Cloud Note",
    },
    "name": {
        "type": "string",
        "description": "Cloud Name",
    },
    "regions": {
        "items": DefinitionsRegion,
        "type": "array",
        "description": "List of regions in this cloud",
    },
    "project_id": {
        "type": "string",
    },
    "id": {
        "type": "integer",
        "description": "Unique ID for the cloud",
    },
    "variables": DefinitionVariablesSource,
}

DefinitionsCloud = {
    "required": [
        "name",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": CloudProperties,
}

DefinitionsCloudId = {
    "type": "object",
    "additionalProperties": False,
    "properties": CloudProperties,
}

DefinitionsCloudCreate = {
    "required": [
        "name",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(CloudProperties,
                                     blacklisted_create_properties),
}

UserProperties = {
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
}

DefinitionUser = {
    "type": "object",
    "additionalProperties": False,
    "properties": UserProperties,
}

DefinitionUserCreate = {
    "required": [
        "username",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(UserProperties,
                                     blacklisted_create_properties),
}

ProjectProperties = {
    "created_at": {
        "type": "string",
    },
    "updated_at": {
        "type": "string",
    },
    "id": {
        "type": "string",
    },
    "name": {
        "type": "string",
    },
    "variables": DefinitionVariablesSource,
}

DefinitionProject = {
    "type": "object",
    "additionalProperties": False,
    "properties": ProjectProperties,
}

DefinitionProjectCreate = {
    "required": [
        "name",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(ProjectProperties,
                                     blacklisted_create_properties),
}

NetworkProperties = {
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
    "cloud_id": {
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
}

DefinitionNetwork = {
    "required": [
        "name",
        "cidr",
        "gateway",
        "netmask",
        "cloud_id",
        "region_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": NetworkProperties,
}

DefinitionNetworkId = {
    "type": "object",
    "additionalProperties": False,
    "properties": NetworkProperties,
}

DefinitionNetworkCreate = {
    "required": [
        "name",
        "cidr",
        "gateway",
        "netmask",
        "cloud_id",
        "region_id",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(NetworkProperties,
                                     blacklisted_create_properties),
}


NetworkInterfaceProperties = {
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
    "properties": NetworkInterfaceProperties,
}

DefinitionNetworkInterfaceId = {
    "type": "object",
    "additionalProperties": False,
    "properties": NetworkInterfaceProperties,
}


DefinitionNetworkInterfaceCreate = {
    "required": [
        "name",
        "device_id",
        "interface_type",
        "ip_address",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(NetworkInterfaceProperties,
                                     blacklisted_create_properties),
}

NetworkDeviceProperties = {
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
    "cloud_id": {
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
    "links": DefinitionLinks,
}

DefinitionNetworkDevice = {
    "required": [
        "name",
        "cloud_id",
        "region_id",
        "device_type",
        "ip_address",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": NetworkDeviceProperties,
}

DefinitionNetworkDeviceId = {
    "type": "object",
    "additionalProperties": False,
    "properties": NetworkDeviceProperties,
}

DefinitionNetworkDeviceCreate = {
    "required": [
        "name",
        "cloud_id",
        "region_id",
        "device_type",
        "ip_address",
    ],
    "type": "object",
    "additionalProperties": False,
    "properties": _remove_properties(NetworkDeviceProperties,
                                     blacklisted_create_properties),
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


def add_pagination_args(resource, args,
                        minimum_page_size=10,
                        default_page_size=30,
                        maximum_page_size=100,
                        marker_type="integer"):
    args.update({
        "limit": {
            "minimum": minimum_page_size,
            "default": default_page_size,
            "maximum": maximum_page_size,
            "type": "integer",
            "description": "Number of {}s to return in a page".format(
                resource,
            ),
        },
        "marker": {
            "type": marker_type,
            "description": "Last {} ID of the previous page".format(
                resource,
            ),
        },
        "sort_dir": {
            "type": "string",
            "enum": ["asc", "desc"],
            "description": ("Direction to sort the {}s based on keys "
                            "specified to sort on.").format(resource),
        },
        "sort_keys": {
            "type": "string",
            "description": "Keys used to sort the {}s by.".format(resource),
        },
    })
    return args


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


DefinitionDevicesPaginated = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "devices": {
            "type": "object",
            "properties": {
                "hosts": {
                    "type": "array",
                    "items": DefinitionsHost,
                },
                "network-devices": {
                    "type": "array",
                    "items": DefinitionNetworkDeviceId,
                },
            },
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
    ("devices", "GET"): {
        "args": {
            "type": "object",
            "additionalProperties": False,
            "properties": add_pagination_args("devices", {
                "region_id": {
                    "type": "integer",
                },
                "cloud_id": {
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
                "descendants": {
                    "default": False,
                    "type": "boolean",
                },
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
                "details": {
                    "default": False,
                    "type": "boolean",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get matching devices",
                },
            }),
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
            "properties": add_pagination_args("region", {
                "name": {
                    "type": "string",
                    "description": "name of the region to get",
                },
                "details": {
                    "type": "boolean",
                    "description": "get detailed information"
                },
                "cloud_id": {
                    "type": "integer",
                    "description": "ID of the cloud to get regions",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a region",
                },
                "id": {
                    "type": "integer",
                    "description": "ID of the region to get",
                },
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            }),
        },
    },
    ("regions", "POST"): {
        "json": DefinitionsRegionCreate,
    },
    ("clouds", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": add_pagination_args("cloud", {
                "name": {
                    "type": "string",
                    "description": "name of the cloud to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a cloud",
                },
                "id": {
                    "type": "integer",
                    "description": "ID of the cloud to get",
                },
                "details": {
                    "default": False,
                    "type": "boolean",
                },
            }),
        },
    },
    ("clouds", "POST"): {
        "json": DefinitionsCloudCreate,
    },
    ("hosts", "POST"): {
        "json": DefinitionHostCreate,
    },
    ("hosts", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": add_pagination_args("host", {
                "name": {
                    "type": "string",
                    "description": "name of the hosts to get",
                },
                "details": {
                    "type": "boolean",
                    "description": "get detailed information",
                },
                "region_id": {
                    "type": "integer",
                    "description": "ID of the region to get hosts",
                },
                "cloud_id": {
                    "type": "integer",
                    "description": "ID of the cloud to get hosts",
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
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            }),
        },
    },
    ("cells_id", "DELETE"): {
    },
    ("cells_id", "GET"): {
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
        "json": DefinitionsCellCreate,
    },
    ("cells", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": add_pagination_args("cell", {
                "region_id": {
                    "type": "string",
                    "description": "name of the region to get cells for",
                },
                "cloud_id": {
                    "type": "integer",
                    "description": "ID of the cloud to get cells",
                },
                "id": {
                    "type": "integer",
                    "description": "id of the cell to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a cell",
                },
                "details": {
                    "type": "boolean",
                    "description": "get detailed information",
                },
                "name": {
                    "type": "string",
                    "description": "name of the cell to get",
                },
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            }),
        },
    },
    ("regions_id", "DELETE"): {
    },
    ("regions_id", "GET"): {
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
    ("clouds_id", "DELETE"): {
    },
    ("clouds_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("clouds_id", "PUT"): {
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
            "properties": add_pagination_args("project", {
                "name": {
                    "default": None,
                    "type": "string",
                    "description": "name of the project to get",
                },
                "vars": {
                    "type": "string",
                    "description": "variable filters to get a project",
                },
                "details": {
                    "default": False,
                    "type": "boolean",
                },
            }, marker_type="string"),
        },
    },
    ("projects", "POST"): {
        "json": DefinitionProjectCreate,
    },
    ("projects_id", "DELETE"): {
    },
    ("projects_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("users", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": add_pagination_args("user", {
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
            }),
        },
    },
    ("users", "POST"): {
        "json": DefinitionUserCreate,
    },
    ("users_id", "DELETE"): {
    },
    ("users_id", "GET"): {
        "args": DefinitionNoParams,
    },
    ("network_devices", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": add_pagination_args("network device", {
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
                "cloud_id": {
                    "type": "integer",
                    "description": "ID of the cloud to get devices",
                },
                "name": {
                    "type": "string",
                    "description": "name of the device to get",
                },
                "details": {
                    "type": "boolean",
                    "description": "get detailed information",
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
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
            }),
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
        "json": DefinitionNetworkDeviceCreate,
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
            "properties": add_pagination_args("network interface", {
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
            }),
        },
    },
    ("network_interfaces", "POST"): {
        "json": DefinitionNetworkInterfaceCreate,
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
            },
        },
    },
    ("networks", "GET"): {
        "args": {
            "additionalProperties": False,
            "properties": add_pagination_args("network", {
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
                "resolved-values": {
                    "default": True,
                    "type": "boolean",
                },
                "details": {
                    "default": False,
                    "type": "boolean",
                    "description": "get detailed information",
                },
            }),
        },
    },
    ("networks", "POST"): {
        "json": DefinitionNetworkCreate,
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
    ("devices", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionDevicesPaginated,
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
    ("clouds", "POST"): {
        201: {
            "headers": None,
            "schema": DefinitionsCloud,
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
    ("clouds", "GET"): {
        200: {
            "headers": None,
            "schema": paginated_resource("clouds", DefinitionsCloud),
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
    ("clouds_id", "GET"): {
        200: {
            "headers": None,
            "schema": DefinitionsCloudId,
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
    ("clouds_id", "PUT"): {
        200: {
            "headers": None,
            "schema": DefinitionsCloudId,
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
    ("clouds_id", "DELETE"): {
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
