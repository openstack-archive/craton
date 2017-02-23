..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============
Listing Devices
===============

https://blueprints.launchpad.net/craton/+spec/list-devices

Craton has separate endpoints for different types of device. Devices of
different types can be linked in a parent-child relationship. Craton does not
offer a mechanism to easily display devices of different types making queries
tracking relationships cumbersome.


Problem description
===================

As a operator I want to be able to list a device's descendants so that I can
visualise or operate on a collection of related devices.

Currently Craton supports two types of devices - hosts and network-devices.
Devices include the optional attribute parent_id to create a parent-child
relationship between two devices. So if one has two network-devices and one is
the parent of the other, the network-devices endpoint can be queried to find
the child device using the ID of the parent, e.g.

  GET /v1/network-devices?parent_id=1

If a third device is added, this time as a child device of the second device,
it is not possible to directly identify it from the root device. A second
query would need to be made using the ID of the second device, e.g.

  GET /v1/network-devices?parent_id=2

This means to represent a complete tree could potentially require a large
number of queries or the client would need to get all the devices and then link
them up itself.

In addition, given that both a host and a network-device can have the same
parent, currently both endpoints need to be queried for any parent_id to get
all the devices.

Proposed change
===============

To meet the needs of the user story and resolve the problems outlined above,
this spec proposes the introduction of a new endpoint for devices to allow for
the querying of devices as a whole.

The endpoint will be /v1/devices and will support:

- querying against a set of attributes common to all devices
- optionally including the descendants of any query

Alternatives
------------

- the traversal of the tree could be left to the client, this would likely be a
  slow process for large deployments
- the existing endpoints, i.e. /v1/hosts and /v1/network-devices, could be
  allowed to return other types of device however this is likely to be
confusing and lead to mistakes uses the output.

Data model impact
-----------------

None

REST API impact
---------------

Endpoint: /v1/devices
Method: GET
Description: List project devices
Normal response code: 200
Expected error response codes: 400

Parameters schema: {
    "type": "object",
    "additionalProperties": False,
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
        "active": {
            "type": "boolean",
        },
        "descendants": {
            "default": False,
            "type": "boolean",
        },
    },
}

Response schema: {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "devices": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "hosts": {
                    "type": "array",
                    "items": DefinitionsHost,
                },
                "network-devices": {
                    "type": "array",
                    "items": DefinitionNetworkDeviceResponse,
                },
            },
        },
        "links": DefinitionsPaginationLinks,
        },
    },
}

Example:
Request
    http://example.com/v1/devices
Response
{
    "devices": {
        "hosts": [
            {
                "active": true,
                "cell_id": 4,
                "created_at": "2017-02-16T14:28:55.000000",
                "device_type": "server",
                "id": 20,
                "ip_address": "192.168.1.20",
                "links": [
                    {
                        "href": "http://example.com/v1/cells/4",
                        "rel": "up"
                    }
                ],
                "name": "host1.DFW.C0002.C-2.example2.com",
                "note": null,
                "parent_id": null,
                "project_id": "b9f10eca-66ac-4c27-9c13-9d01e65f96b4",
                "region_id": 2,
                "updated_at": null
            }
            ... more hosts ...,
        ],
        "network-devices": [
            {
                "access_secret_id": null,
                "active": true,
                "cell_id": 4,
                "created_at": "2017-02-16T14:28:55.000000",
                "device_type": "switch",
                "id": 16,
                "ip_address": "10.10.1.1",
                "links": [
                    {
                        "href": "http://example.com/v1/cells/4",
                        "rel": "up"
                    }
                ],
                "model_name": "model-x",
                "name": "switch1.C0002.DFW.example.com",
                "os_version": "version-1",
                "parent_id": null,
                "project_id": "b9f10eca-66ac-4c27-9c13-9d01e65f96b4",
                "region_id": 2,
                "updated_at": null,
                "vlans": null
            },
            ... more network-devices ...,
        ],
    },
    "links": [
        {
            "href": "http://example.com/v1/devices?sort_dir=asc&limit=30&sort_keys=created_at%2Cid",
            "rel": "first"
        },
        {
            "href": "http://example.com/v1/devices?sort_dir=asc&limit=30&sort_keys=created_at%2Cid",
            "rel": "prev"
        },
        {
            "href": "http://example.com/v1/devices?sort_dir=asc&limit=30&sort_keys=created_at%2Cid",
            "rel": "self"
        },
        {
            "href": "http://example.com/v1/devices?sort_dir=asc&limit=30&sort_keys=created_at%2Cid&marker=20",
            "rel": "next"
        }
    ]
}

Example:
Request
    http://example.com/v1/devices?parent_id=16&descendants=true
Response
{
    "devices": {
        "network-devices": [
            {
                "access_secret_id": null,
                "active": true,
                "cell_id": 4,
                "created_at": "2017-02-16T14:28:55.000000",
                "device_type": "switch",
                "id": 17,
                "ip_address": "10.10.1.2",
                "links": [
                    {
                        "href": "http://example.com/v1/network-devices/16",
                        "rel": "up"
                    }
                ],
                "model_name": "model-x",
                "name": "switch2.C0002.DFW.example.com",
                "os_version": "version-1",
                "parent_id": 16,
                "project_id": "b9f10eca-66ac-4c27-9c13-9d01e65f96b4",
                "region_id": 2,
                "updated_at": null,
                "vlans": null
            },
            {
                "access_secret_id": null,
                "active": true,
                "cell_id": 4,
                "created_at": "2017-02-16T14:28:55.000000",
                "device_type": "switch",
                "id": 18,
                "ip_address": "10.10.1.3",
                "links": [
                    {
                        "href": "http://example.com/v1/network-devices/17",
                        "rel": "up"
                    }
                ],
                "model_name": "model-x",
                "name": "switch3.C0002.DFW.example.com",
                "os_version": "version-1",
                "parent_id": 17,
                "project_id": "b9f10eca-66ac-4c27-9c13-9d01e65f96b4",
                "region_id": 2,
                "updated_at": null,
                "vlans": null
            },
        ],
        "hosts": [
            {
                "active": true,
                "cell_id": 4,
                "created_at": "2017-02-16T14:28:55.000000",
                "device_type": "server",
                "id": 200,
                "ip_address": "192.168.1.20",
                "links": [
                    {
                        "href": "http://example.com/v1/network-devices/16",
                        "rel": "up"
                    }
                ],
                "name": "host10.DFW.C0002.C-2.example2.com",
                "note": null,
                "parent_id": 16,
                "project_id": "b9f10eca-66ac-4c27-9c13-9d01e65f96b4",
                "region_id": 2,
                "updated_at": null
            },
        ],
    },
    "links": [
        {
            "href": "http://example.com/v1/devices?parent_id=16&descendants=true&sort_dir=asc&limit=30&sort_keys=created_at%2Cid",
            "rel": "first"
        },
        {
            "href": "http://example.com/v1/devices?parent_id=16&descendants=true&sort_dir=asc&limit=30&sort_keys=created_at%2Cid",
            "rel": "prev"
        },
        {
            "href": "http://example.com/v1/devices?parent_id=16&descendants=true&sort_dir=asc&limit=30&sort_keys=created_at%2Cid",
            "rel": "self"
        },
        {
            "href": "http://example.com/v1/devices?parent_id=16&descendants=true&sort_dir=asc&limit=30&sort_keys=created_at%2Cid&marker=20",
            "rel": "next"
        }
    ]
}

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

- /v1/devices with need to be supported by the client.

Performance Impact
------------------

Given the nature of this new endpoint, there is a strong likelihood that it
will be used for most requests where listing devices is required, even if the
user is only after one type.

Other deployer impact
---------------------

None

Developer impact
----------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
- git-harry

Other contributors:
- None

Work Items
----------

- add /v1/devices endpoint

Dependencies
============

None

Testing
=======

A full set of functional and unit tests will need to be added.

Documentation Impact
====================

The repo documentation will require updating but this is handled by the
project.

References
==========

None
