.. _hosts:

=====
Hosts
=====

Definition of host

Create Host
===========

:POST: /v1/hosts

Create a new host

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| data       | body | object  | User defined data             |
+------------+------+---------+-------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Create Host**

 ..literalinclude:: ./api_samples/hosts/hosts-create-req.json
    :language: javascript

Response
--------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| host       | body | object  | - id                          |
|            |      |         | - name                        |
|            |      |         | - cell_id                     |
|            |      |         | - region_id                   |
|            |      |         | - parent_id                   |
|            |      |         | - ip_address                  |
|            |      |         | - device_type                 |
|            |      |         | - active                      |
|            |      |         | - labels                      |
|            |      |         | - note                        |
|            |      |         | - data                        |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the host         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| data       | body | object  | User defined data             |
+------------+------+---------+-------------------------------+

.. todo:: **Example Create Host**

 ..literalinclude:: ./api_samples/hosts/hosts-create-resp.json
    :language: javascript

List Hosts
==========

:GET: /v1/hosts?region_id=

Gets all Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Default response: unexpected error

Request
-------

+------------+------+---------+---------+------------------------------+
| Name       | In   | Type    | Required| Description                  |
+============+======+=========+=========+==============================+
| region_id  | query| integer | Yes     | ID of the region to get hosts|
+------------+------+---------+---------+------------------------------+
| limit      | query| integer | No      | Number of host to return     |
|            |      |         |         | Ranging from 1 - 10000       |
+------------+------+---------+---------+------------------------------+
| name       | query| string  | No      | Name of the host to get      |
+------------+------+---------+---------+------------------------------+
| cell_id    | query| integer | No      | Name of the cell to get      |
+------------+------+---------+---------+------------------------------+
| ip         | query| string  | No      | IP address of the host to get|
+------------+------+---------+---------+------------------------------+
| device_type| query| string  | No      | Type of host to get          |
+------------+------+---------+---------+------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| hosts      | body | array   | array of host                 |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the host         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| data       | body | object  | User defined data             |
+------------+------+---------+-------------------------------+

.. todo:: **Example List Host**

 ..literalinclude:: ./api_samples/hosts/hosts-list-resp.json
     :language: javascript

.. todo:: **Example Unexpected Error**

 ..literalinclude:: ./api_samples/errors/errors-unexpected-resp.json
    :language: javascript

Update Hosts
============

:PUT: /v1/hosts/{id}

Update an existing host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

+------------+------+---------+------------------------------------+
| Name       | In   | Type    | Description                        |
+============+======+=========+====================================+
| name       | body | string  | Unique name of the host            |
+------------+------+---------+------------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell       |
+------------+------+---------+------------------------------------+
| region_id  | body | integer | Unique ID of the host's region     |
+------------+------+---------+------------------------------------+
| parent_id  | body | integer | ID of the host's parent            |
+------------+------+---------+------------------------------------+
| ip_address | body | string  | IP address of the host             |
+------------+------+---------+------------------------------------+
| device_type| body | string  | Type of host                       |
+------------+------+---------+------------------------------------+
| active     | body | boolean | State of host                      |
+------------+------+---------+------------------------------------+
| labels     | body | string  | User defined labels                |
+------------+------+---------+------------------------------------+
| note       | body | string  | Note used for governance           |
+------------+------+---------+------------------------------------+
| data       | body | object  | User defined data                  |
+------------+------+---------+------------------------------------+
| id         | path | integer | Unique ID of the host to be updated|
+------------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Update Host**

 ..literalinclude:: ./api_samples/hosts/hosts-update-req.json
    :language: javascript

Response
--------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| host       | body | object  | - id                          |
|            |      |         | - name                        |
|            |      |         | - cell_id                     |
|            |      |         | - region_id                   |
|            |      |         | - parent_id                   |
|            |      |         | - ip_address                  |
|            |      |         | - device_type                 |
|            |      |         | - active                      |
|            |      |         | - labels                      |
|            |      |         | - note                        |
|            |      |         | - data                        |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the host         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| data       | body | object  | User defined data             |
+------------+------+---------+-------------------------------+

.. todo:: **Example Update Host**

  ..literalinclude:: ./api_samples/hosts/hosts-update-resp.json
     :language: javascript

Update Host Data
================

:PUT: /v1/hosts/{id}/data

Update user defined data for the host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

+--------+------+---------+------------------------------------+
| Name   | In   | Type    | Description                        |
+========+======+=========+====================================+
| key    | body | string  | Identifier                         |
+--------+------+---------+------------------------------------+
| value  | body | object  | Data                               |
+--------+------+---------+------------------------------------+
| id     | path | integer | Unique ID of the host to be updated|
+--------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Update Host Data**

 ..literalinclude:: ./api_samples/hosts/hosts-upadate—data-req.json
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


.. todo:: **Example Update Host Data**

 ..literalinclude:: ./api_samples/hosts/hosts-update-data-resp.json
    :language: javascript

Delete Host
===========

:DELETE: /v1/hosts/{id}

Deletes an existing record of a Host

Normal response codes: no content(204)

Error response codes: invalid request(400), host not found(404)

Request
-------

+--------+------+---------+------------------------------------+
| Name   | In   | Type    | Description                        |
+========+======+=========+====================================+
| id     | path | integer | Unique ID of the host to be deleted|
+--------+------+---------+------------------------------------+

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

:DELETE: /v1/hosts/{id}/data

Delete existing key/value data for the Host

Normal response codes: no content(204)

Error response codes: invalid request(400), host not found(404) validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| id     | path | integer | Unique ID of the host   |
+--------+------+---------+-------------------------+
| key    | body | string  | Identifier to be deleted|
+--------+------+---------+-------------------------+
| value  | body | object  | Data to be deleted      |
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
