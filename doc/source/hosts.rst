.. _hosts:

=====
Hosts
=====

Definition of host

Create Host
============

.. glossary:: 
    POST 
        /v1/hosts

Create a new host

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| name       | body | string  | Unique name of the host |
+------------+------+---------+-------------------------+
| region_id  | body | integer | Unique ID of the region |
+------------+------+---------+-------------------------+
| project_id | body | integer | ID of the project       |
+------------+------+---------+-------------------------+
| ip_address | body | string  | IP address of host      |
+------------+------+---------+-------------------------+
| device_type| body | string  | Type of host            |
+------------+------+---------+-------------------------+  

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Create Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-create-req.json
   :language: javascript

Response
--------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| host       | body | object  | - host_id               |
|            |      |         | - name                  |
|            |      |         | - cell_id               |
|            |      |         | - region_id             |
|            |      |         | - parent_id             |
|            |      |         | - project_id            |
|            |      |         | - ip_address            |
|            |      |         | - device_type           |
|            |      |         | - labels                |
|            |      |         | - note                  |
|            |      |         | - data                  |
+------------+------+---------+-------------------------+
| host_id    | body | object  | Unique ID of the host   |
+------------+------+---------+-------------------------+
| name       | body | object  | Unique name of the host |
+------------+------+---------+-------------------------+
| cell_id    | body | object  | Unique ID of the cell   |
+------------+------+---------+-------------------------+
| region_id  | body | object  | Unique ID of the region |
+------------+------+---------+-------------------------+
| parent_id  | body | object  | Parent ID of this host  |
+------------+------+---------+-------------------------+
| project_id | body | integer | ID of the project       |
+------------+------+---------+-------------------------+
| ip_address | body | string  | IP address of host      |
+------------+------+---------+-------------------------+
| device_type| body | string  | Type of host            |
+------------+------+---------+-------------------------+
| labels     | body | string  | User defined labels     |
+------------+------+---------+-------------------------+
| note       | body | string  | Note used for governance|
+------------+------+---------+-------------------------+
| data       | body | object  | User defined data       |
+------------+------+---------+-------------------------+

**Example Create Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-create-resp.json
   :language: javascript

List Hosts
==========

.. glossary::  
    GET 
        /v1/hosts

Gets all Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Default response: unexpected error

Request
--------

+------------+------+---------+-----------------------------------+
| Name       | In   | Type    | Description                       |
+============+======+=========+===================================+
| limit      | query| string  | Number of host to return          |
|            |      |         | Ranging from 1 - 10000            |
+------------+------+---------+-----------------------------------+
| name       | query| string  | Name of host to get               |
+------------+------+---------+-----------------------------------+
| host_id    | query| integer | ID of the host to get             |
+------------+------+---------+-----------------------------------+
| region     | query| string  | Name of the region to get         |
+------------+------+---------+-----------------------------------+
| cell       | query| string  | Name of the cell to get           |
+------------+------+---------+-----------------------------------+
| ip_address | query| string  | IP address to get                 |
+------------+------+---------+-----------------------------------+
| service    | query| string  | Openstack service to query gost by|
+------------+------+---------+-----------------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

Response
--------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| hosts      | body | array   | array of host           |
+------------+------+---------+-------------------------+
| host_id    | body | object  | Unique ID of the host   |
+------------+------+---------+-------------------------+
| name       | body | object  | Unique name of the host |
+------------+------+---------+-------------------------+
| cell_id    | body | object  | Unique ID of the cell   |
+------------+------+---------+-------------------------+
| region_id  | body | object  | Unique ID of the region |
+------------+------+---------+-------------------------+
| parent_id  | body | object  | Parent ID of this host  |
+------------+------+---------+-------------------------+
| project_id | body | integer | ID of the project       |
+------------+------+---------+-------------------------+
| ip_address | body | string  | IP address of host      |
+------------+------+---------+-------------------------+
| device_type| body | string  | Type of host            |
+------------+------+---------+-------------------------+
| labels     | body | string  | User defined labels     |
+------------+------+---------+-------------------------+
| note       | body | string  | Note used for governance|
+------------+------+---------+-------------------------+
| data       | body | object  | User defined data       |
+------------+------+---------+-------------------------+

**Example List Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-list-resp.json
   :language: javascript

**Example Unexpected Error**

..literalinclude:: ../../doc/api_samples/errors/errors-unexpected-resp.json
   :language: javascript

Update Hosts
============

.. glossary::
    PUT 
        /v1/hosts/{host_id}

Update an existing host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| host_id    | body | object  | Unique ID of the host   |
+------------+------+---------+-------------------------+
| name       | body | object  | Unique name of the host |
+------------+------+---------+-------------------------+
| cell_id    | body | object  | Unique ID of the cell   |
+------------+------+---------+-------------------------+
| region_id  | body | object  | Unique ID of the region |
+------------+------+---------+-------------------------+
| parent_id  | body | object  | Parent ID of this host  |
+------------+------+---------+-------------------------+
| project_id | body | integer | ID of the project       |
+------------+------+---------+-------------------------+
| ip_address | body | string  | IP address of host      |
+------------+------+---------+-------------------------+
| device_type| body | string  | Type of host            |
+------------+------+---------+-------------------------+
| labels     | body | string  | User defined labels     |
+------------+------+---------+-------------------------+
| note       | body | string  | Note used for governance|
+------------+------+---------+-------------------------+
| data       | body | object  | User defined data       |
+------------+------+---------+-------------------------+
| host_id    | path | integer | Unique ID of the host   |
+------------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Update Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-update-req.json
   :language: javascript

Response
--------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| host       | body | object  | - host_id               |
|            |      |         | - name                  |
|            |      |         | - cell_id               |
|            |      |         | - region_id             |
|            |      |         | - parent_id             |
|            |      |         | - project_id            |
|            |      |         | - ip_address            |
|            |      |         | - device_type           |
|            |      |         | - labels                |
|            |      |         | - note                  |
|            |      |         | - data                  |
+------------+------+---------+-------------------------+
| host_id    | body | object  | Unique ID of the host   |
+------------+------+---------+-------------------------+
| name       | body | object  | Unique name of the host |
+------------+------+---------+-------------------------+
| cell_id    | body | object  | Unique ID of the cell   |
+------------+------+---------+-------------------------+
| region_id  | body | object  | Unique ID of the region |
+------------+------+---------+-------------------------+
| parent_id  | body | object  | Parent ID of this host  |
+------------+------+---------+-------------------------+
| project_id | body | integer | ID of the project       |
+------------+------+---------+-------------------------+
| ip_address | body | string  | IP address of host      |
+------------+------+---------+-------------------------+
| device_type| body | string  | Type of host            |
+------------+------+---------+-------------------------+
| labels     | body | string  | User defined labels     |
+------------+------+---------+-------------------------+
| note       | body | string  | Note used for governance|
+------------+------+---------+-------------------------+
| data       | body | object  | User defined data       |
+------------+------+---------+-------------------------+

**Example Update Host**  (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-update-resp.json
   :language: javascript

Update Host Data
==================

.. glossary:: 
    PUT 
        /v1/hosts/{host_id}/data

Update user defined data for the host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| key    | body | string  | Identifier              |
+--------+------+---------+-------------------------+
| value  | body | object  | Data                    |
+--------+------+---------+-------------------------+
| host_id| path | integer | Unique ID of the host   |
+--------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Update Host Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-upadate—data-req.json
   :language: javascript

Response
--------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| key    | body | string  | Identifier              |
+--------+------+---------+-------------------------+
| value  | body | object  | Data                    |
+--------+------+---------+-------------------------+


**Example Update Host Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-update-data-resp.json
   :language: javascript

Delete Host
===========

.. glossary:: 
    DELETE 
        /v1/hosts/{host_id}

Deletes an existing record of a Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| host_id| path | integer | Unique ID of the host   |
+--------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Host Data
================

.. glossary:: 
    DELETE 
        /v1/hosts/{host_id}/data

Delete existing key/value data for the Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404) validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| host_id| path | integer | Unique ID of the host   |
+--------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
