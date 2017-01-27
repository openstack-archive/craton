..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Adjust Variables API to Improve Usability
==========================================

https://blueprints.launchpad.net/craton/+spec/variables-api

The variables API conflicts with RFC 2616 [1] and the guidance provided by
API-WG [2] as well as making it difficult to see where a variable is set.


Problem description
===================

The variables API, in a number of ways, does not conform with RFC 2616 or the
API-WG guidelines:

- While the current implementation is functional, its divergence from the
appropriate standards does not offer any technical advantage. For example,
partial updates with PUT or DELETE requests including a request body.

- The response body of a PUT request includes the resource variables but this
isn't sufficient information to understand the current resolved variables for
that resource.

- With a GET request it is possible to see the resource variables or the
resolved variables, but it is difficult to work out what will happen if a
resource variable is removed because it may also be set in one or more of the
resource's ancestors. Also it is only possible to tell what the variables
object relates to from the request because the same key "variables" is always
used.

The following are examples of the hosts variables API, with details of areas
that may benefit from redesign:

GET /hosts/<id>/variables
# curl 'http://127.0.0.1:8080/v1/hosts/2/variables' \
-H "Content-Type: application/json" \
-H "X-Auth-Token: demo" \
-H "X-Auth-User: demo" \
-H "X-Auth-Project: b9f10eca66ac4c279c139d01e65f96b4" \
-s | python -m json.tool
{
    "variables": {
        "cell": 1,
        "host": 1,
        "region": 1
    }
}


- A GET request returns resolved variables, this sets it apart from DELETE and
PUT in that the default action does not relate specifically to host variables.
- The variables object in the response can represent either the resource
variables or the resolved variables, its type is only know at request time.
This creates the potential for mistakes.
- The request isn't sufficient to understand what will happen if a host
variable is removed. The end-user needs to either try it or work out all the
ancestors and query them separately.

PUT /hosts/<id>/variables
# curl 'http://127.0.0.1:8080/v1/hosts/2/variables' \
-H "Content-Type: application/json" \
-H "X-Auth-Token: demo" \
-H "X-Auth-User: demo" \
-H "X-Auth-Project: b9f10eca66ac4c279c139d01e65f96b4" \
-s -XPUT -d'{"host2": 2}' | python -m json.tool
{
    "variables": {
        "host": 1,
        "host2": 2
    }
}


- PUT should include the entire resource in the request, currently only
variables being modified are required. The body of this request does not have
to be a complete representation of the data, missing fields are not
removed/updated.
- The returned data does not show how resolved values will have been impacted
and so this data is of limited use.

DELETE /hosts/<id>/variables
# curl 'http://127.0.0.1:8080/v1/hosts/2/variables' \
-H "Content-Type: application/json" \
-H "X-Auth-Token: demo" \
-H "X-Auth-User: demo" \
-H "X-Auth-Project: b9f10eca66ac4c279c139d01e65f96b4" \
-s -XDELETE -d'{"_": "host", "_2": "region"}' -i
HTTP/1.0 204 NO CONTENT
Date: Thu, 26 Jan 2017 14:49:37 GMT
Server: WSGIServer/0.2 CPython/3.5.2
Content-Type: application/json
Content-Length: 0
x-openstack-request-id: req-37fb37e7-6013-4ddd-8dcb-beb51b4cf392

# curl 'http://127.0.0.1:8080/v1/hosts/2/variables' \
-H "Content-Type: application/json" \
-H "X-Auth-Token: demo" \
-H "X-Auth-User: demo" \
-H "X-Auth-Project: b9f10eca66ac4c279c139d01e65f96b4" \
-s | python -m json.tool
{
    "variables": {
        "cell": 1,
        "region": 1
    }
}

- DELETE should not include an entity body
- DELETE should delete all variables and not a subset; PUT or PATCH should be
used to modify the variables
- DELETE requires a key/value pair where the key is unused and the value is the
key to be deleted, this does not seem intuitive
- Only keys in the top level object can be deleted.
- Keys that don't exist are ignored, this might lead to mistakes if the user
mistakes resolved variables for resource variables.
- DELETE only deletes variables on the resource so the resource may still have
variables that have been inherited, this is not obvious when a 204 is returned
with no response body.

Proposed change
===============

The API for managing variables should be updated to better align with other
OpenStack projects, as defined by the API-WG guidelines and the appropriate
RFCs. More variables information should also be provided in responses so that
there is sufficient context to understand the impact of any change and
distinguish between types of variables.

The proposed changes will impact all resources that have variables, these
resources are:

- cells
- hosts
- networks
- network devices
- regions

These changes amount to adjusting the API so will be detailed in `REST API
impact`_ but to summarise:
- GET requests should return both resource and resolved values by default and
  the complete hierarchy if requested.
- PUT should be removed and replaced with PATCH.
- DELETE should only be used to delete all variables associated with a resource
  and return remaining resolved variables.

Alternatives
------------

Each of these alternatives does not necessarily represent a complete solution,
it may only refer to one aspect of it.

- Keep the current implementation
  - Given the differences between the API and the expectation of OpenStack and
    RFC 2616, keeping the current implementation, on a project that is yet to
    release version 1 seems only to present risks given those design decisions
    are not specifically required by the project.

- Use both PUT and PATCH
  - Given the overlapping nature of the two methods, retaining PUT appears to
    simply introduce an additional maintenance burden.

- Update PUT to require a complete representation of the resource
  - This is the current API-WG guidance for metadata. Metadata values, in
    general, appear to be strings. Craton variables can be complex object of
    varying sizes and so using PATCH should provide a more efficient mechanism
    and provides a standard way for the client to define what has changed.

- Individually addressable variables
  - Where resources have a lot of variables, this has the potential to create a
    large overhead due to the number of additional API call that would be
    required.

- Flip the default value for resolved-variables
  - This still requires knowledge of the request to understand what type of
    variables have been returned and does not help determining the impact of
    changes.

Data model impact
-----------------

None

REST API impact
---------------

- GET /v1/<resource>/<id>

  Example:
    Request:
      URL: /v1/hosts/1
      Method: GET

    Response:
      Status code: 200
      Body:
        {
            "active": true,
            "cell_id": 1,
            "created_at": "2017-01-01T12:34:56.000000",
            "device_type": "server",
            "id": 1,
            "ip_address": "192.0.2.1",
            "name": "host0.example1.com",
            "note": null,
            "project_id": "a3e40557-53af-4f99-8a5d-feefc9ac04eb",
            "region_id": 1,
            "updated_at": null,
            "resource_variables": {
                "hostvar1": true,
            },
            "resolved_variables": {
                "hostvar1": true,
                "cellvar1": true,
                "regionvar1": true,
            },
        }

- GET /v1/<resource>/<id>/variables

  Example:
    Request:
      URL: /v1/hosts/1/variables
      Method: GET

    Response:
      Status code: 200
      Body:
        {
            "resource_variables": {
                "hostvar1": true,
            },
            "resolved_variables": {
                "hostvar1": true,
                "cellvar1": true,
                "regionvar1": true,
            },
        }

  Example:
    Request:
      URL: /v1/hosts/1/variables?ancestors=true
      Method: GET

    Response:
      Status code: 200
      Body:
        {
            "ancestors_variables": [
              {
                "resource_variables": {
                "cellvar1": true,
                "overridden2: true,
                },
                "resource": "/v1/cells/1",
              },
              {
                "resource_variables": {
                "regionvar1": true,
                "overridden1: false,
                "overridden2: false,
                }
                "resource": "/v1/regions/1",
              },
            ]
            "resource_variables": {
                "hostvar1": true,
                "overridden1: true,
            },
            "resolved_variables": {
                "hostvar1": true,
                "cellvar1": true,
                "regionvar1": true,
                "overridden1: true,
                "overridden2: true,
            },
        }

- PUT /v1/<resource>/<id>/variables

  Remove from API.

- PATCH /v1/<resource>/<id>/variables

  Request body:
    {
        "operations": []
    {
    Where operations is a JSON patch document as defined by RFC 6902 [1] and
    implemented by python-json-patch [3].

  Response body: variables resource.
        {
            "resource_variables": {
            },
            "resolved_variables": {
            },
        }

  Response status code: 200

  Example:
    Request:
      URL: /v1/hosts/1/variables
      Method: PATCH
      Body:
        {
            "operations": [
                {"op": "add", "path": "/hostvar2", "value": "newvar"},
            ],
        }

    Response:
      Status code: 200
      Body:
        {
            "resource_variables": {
                "hostvar1": true,
                "hostvar2": "newvar",
            },
            "resolved_variables": {
                "hostvar1": true,
                "hostvar2": "newvar",
                "cellvar1": true,
                "regionvar1": true,
            },
        }

- DELETE /v1/<resource>/<id>/variables

  Request body: None

  Example:
    Request:
      URL: /v1/hosts/1/variables
      Method: DELETE

    Response:
      Status code: 200
      Body:
        {
            "resource_variables": {},
            "resolved_variables": {
                "cellvar1": true,
                "regionvar1": true,
            },
        }

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Given that v1 of the API has not yet been released, the changes should not
impact the end-user beyond what would normally expected for an API design that
has not yet been finalised.

Performance Impact
------------------

None

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

- implement GET changes
- implement PUT/PATCH changes
- implement DELETE changes


Dependencies
============

None


Testing
=======

Given that this spec seeks to modify an existing interface, updating existing
unit and functional tests should be sufficient to cover this change.


Documentation Impact
====================

The API documentation will require changes to reflect the new interface.


References
==========

[1] https://tools.ietf.org/html/rfc6902
[2] https://specs.openstack.org/openstack/api-wg/index.html
[3] https://github.com/stefankoegl/python-json-patch
