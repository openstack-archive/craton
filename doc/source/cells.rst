.. _cells:

=====
Cells
=====

Definition of cell

Create Cell
===========
.. glossary::
    POST
        /v1/cells

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
| id         | body | integer | Unique ID of the cell   |
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

**Example Create Cell** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-create-req.json
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

**Example Create Cell** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-create-resp.json
   :language: javascript

List Cells
==========

.. glossary::
    GET
        /v1/cells?region_id=

Gets all Cells

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Default response: unexpected error

Request
-------

+-----------+-------+--------+---------+----------------------------------+
| Name      | In    | Type   | Required| Description                      |
+===========+=======+========+=========+==================================+
| id        | query | integer| Yes     | ID of the cell to get            |
+-----------+-------+--------+---------+----------------------------------+
| name      | query | string | No      | Name of the cell to get          |
+-----------+-------+--------+--------------------------------------------+
| region_id | query | string | No      | ID of the region to get cells for|
+-----------+-------+---------+-------------------------------------------+

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

**Example List Cells** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-list-resp.json
   :language: javascript 

**Example Unexpected Error** (TO-DO)

..literalinclude:: ../../doc/api_samples/errors/errors-unexpected-resp.json
   :language: javascript

Update Cells
============

.. glossary::
    PUT
        /v1/cells/{cell_id}

Update an existing cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Request
-------

+----------+------+---------+-------------------------------+
| Name     | In   | Type    | Description                   |
+==========+======+=========+===============================+
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
| cell_id  | path | integer | Unique ID of the cell         |
+----------+------+---------+-------------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Update Cell** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-update-req.json
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

**Example Update Cell**  (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-update-resp.json
   :language: javascript

Update Cell Data
================

.. glossary::
    PUT
        /v1/cells/{cell_id}/data

Update user defined data for the cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| key    | body | string  | Identifier              |
+--------+------+---------+-------------------------+
| value  | body | object  | Data                    |
+--------+------+---------+-------------------------+
| cell_id| path | integer | Unique ID of the cell   |
+--------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Update Cell Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-upadate—data-req.json
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

**Example Update Cell Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-update-data-resp.json
   :language: javascript

Delete Cell
===========

.. glossary::
    DELETE
        /v1/cells/{cell_id}

Deletes an existing record of a Cell

Normal response codes: no content(204)

Error response codes: invalid request(400), cell not found(404)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| cell_id| path | integer | Unique ID of the cell   |
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

Delete Cell Data
================

.. glossary::
    DELETE
        /v1/cells/{cell_id}/data

Delete existing key/value data for the cell

Normal response codes: no content(204)

Error response codes: invalid request(400), cell not found(404) validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| cell_id| path | integer | Unique ID of the cell   |
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
