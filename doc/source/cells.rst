.. _cells:

=====
Cells
=====

Definition of cell

Create Cell
===========
:POST: /v1/cells

Create a new Cell

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| name       | boody| string  | Unique name of the cell |
+------------+------+---------+-------------------------+
| region_id  | body | integer | Unique ID of the region |
+------------+------+---------+-------------------------+
| labels     | body | string  | User defined labels     |
+------------+------+---------+-------------------------+
| note       | body | string  | Note used for governance|
+------------+------+---------+-------------------------+
| data       | body | object  | User defined data       |
+------------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Create Cell**

 ..literalinclude:: ./doc/api_samples/cells/cells-create-req.json
    :language: javascript

Response
--------

+-----------+------+---------+-------------------------------+
| Name      | In   | Type    | Description                   |
+===========+======+=========+===============================+
| cell      | body | object  | - id                          |
|           |      |         | - name                        |
|           |      |         | - region_id                   |
|           |      |         | - labels                      |
|           |      |         | - note                        |
|           |      |         | - data                        |
+-----------+------+---------+-------------------------------+
| id        | body | integer | Unique ID of the cell         |
+-----------+------+---------+-------------------------------+
| name      | body | string  | Unique name of the cell       |
+-----------+------+---------+-------------------------------+
| region_id | body | integer | Unique ID of the cell's region|
+-----------+------+---------+-------------------------------+
| labels    | body | string  | User defined labels           |
+-----------+------+---------+-------------------------------+
| note      | body | string  | Note used for governance      |
+-----------+------+---------+-------------------------------+
| data      | body | object  | User defined data             |
+-----------+------+---------+-------------------------------+

.. todo:: **Example Create Cell**

 ..literalinclude:: ./doc/api_samples/cells/cells-create-resp.json
    :language: javascript

List Cells
==========

:GET: /v1/cells?region_id=

Gets all Cells

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Default response: unexpected error

Request
-------

+-----------+-------+--------+---------+----------------------------------+
| Name      | In    | Type   | Required| Description                      |
+===========+=======+========+=========+==================================+
| region_id | query | string | No      | ID of the region to get cells for|
+-----------+-------+--------+---------+----------------------------------+

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
| cells      | body | array   | Array of cell objects         |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the cell         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the cell       |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the cell's region|
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| data       | body | object  | User defined data             |
+------------+------+---------+-------------------------------+

.. todo:: **Example List Cells**

 ..literalinclude:: ./doc/api_samples/cells/cells-list-resp.json
    :language: javascript

.. todo:: **Example Unexpected Error**

 ..literalinclude:: ./api_samples/errors/errors-unexpected-resp.json
    :language: javascript

Update Cells
============

:PUT: /v1/cells/{id}

Update an existing cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Request
-------

+----------+------+---------+------------------------------------+
| Name     | In   | Type    | Description                        |
+==========+======+=========+====================================+
| name     | body | string  | Unique name of the cell            |
+----------+------+---------+------------------------------------+
| region_id| body | integer | Unique ID of the cell's region     |
+----------+------+---------+------------------------------------+
| labels   | body | string  | User defined labels                |
+----------+------+---------+------------------------------------+
| note     | body | string  | Note used for governance           |
+----------+------+---------+------------------------------------+
| data     | body | object  | User defined data                  |
+----------+------+---------+------------------------------------+
| id       | path | integer | Unique ID of the cell to be updated|
+----------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Update Cell**

 ..literalinclude:: ./api_samples/cells/cells-update-req.json
    :language: javascript

Response
--------

+----------+------+---------+-------------------------------+
| Name     | In   | Type    | Description                   |
+==========+======+=========+===============================+
| cell     | body | object  | - id                          |
|          |      |         | - name                        |
|          |      |         | - region_id                   |
|          |      |         | - labels                      |
|          |      |         | - note                        |
|          |      |         | - data                        |
+----------+------+---------+-------------------------------+
| id       | body | integer | Unique ID of the cell         |
+----------+------+---------+-------------------------------+
| name     | body | string  | Unique name of the cell       |
+----------+------+---------+-------------------------------+
| region_id| body | integer | Unique ID of the cell's region|
+----------+------+---------+-------------------------------+
| labels   | body | string  | User defined labels           |
+----------+------+---------+-------------------------------+
| note     | body | string  | Note used for governance      |
+----------+------+---------+-------------------------------+
| data     | body | object  | User defined data             |
+----------+------+---------+-------------------------------+

.. todo:: **Example Update Cell**

 ..literalinclude:: ./api_samples/cells/cells-update-resp.json
   :language: javascript

Update Cell Data
================

:PUT: /v1/cells/{id}/data

Update user defined data for the cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Request
-------

+--------+------+---------+------------------------------------+
| Name   | In   | Type    | Description                        |
+========+======+=========+====================================+
| key    | body | string  | Identifier                         |
+--------+------+---------+------------------------------------+
| value  | body | object  | Data                               |
+--------+------+---------+------------------------------------+
| id     | path | integer | Unique ID of the cell to be updated|
+--------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Update Cell Data**

 ..literalinclude:: ./api_samples/cells/cells-upadate—data-req.json
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

.. todo:: **Example Update Cell Data**

 ..literalinclude:: ./api_samples/cells/cells-update-data-resp.json
    :language: javascript

Delete Cell
===========

:DELETE: /v1/cells/{id}

Deletes an existing record of a Cell

Normal response codes: no content(204)

Error response codes: invalid request(400), cell not found(404)

Request
-------

+--------+------+---------+------------------------------------+
| Name   | In   | Type    | Description                        |
+========+======+=========+====================================+
| id     | path | integer | Unique ID of the cell to be deleted|
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

Delete Cell Data
================

:DELETE: /v1/cells/{id}/data

Delete existing key/value data for the cell

Normal response codes: no content(204)

Error response codes: invalid request(400), cell not found(404) validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| id     | path | integer | Unique ID of the cell   |
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
