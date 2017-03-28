.. _cells:

=====
Cells
=====

Definition of cell

Create Cell
===========
:POST: /v1/cells

Create a new Cell

Normal response codes: OK(201)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+------------+------+---------+-------------------------+
| Name       | In   | Type    | Description             |
+============+======+=========+=========================+
| name       | body | string  | Unique name of the cell |
+------------+------+---------+-------------------------+
| region_id  | body | integer | Unique ID of the region |
+------------+------+---------+-------------------------+
| labels     | body | string  | User defined labels     |
+------------+------+---------+-------------------------+
| note       | body | string  | Note used for governance|
+------------+------+---------+-------------------------+
| variables  | body | object  | User defined variables  |
+------------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Cell Create
*******************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/cells" \
        -d '{"name": "myCell", "region_id": 1}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

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
|           |      |         | - variables                   |
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
| variables | body | object  | User defined variables        |
+-----------+------+---------+-------------------------------+

Example Cell Create
*******************

.. code-block:: json

   {
      "id": 1,
      "name": "myCell",
      "note": null,
      "region_id": 1
   }
 
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
| region_id | query | string | Yes     | ID of the region to get cells for|
+-----------+-------+--------+---------+----------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Cell List
*****************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/cells?region_id=1" \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

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
| variables  | body | object  | User defined variables        |
+------------+------+---------+-------------------------------+

Example Cell List
*****************

.. code-block:: json

   [
      {
         "id": 2,
         "name": "cellJr",
         "note": null,
         "region_id": 1
      },
      {
         "id": 1,
         "name": "myCell",
         "note": null,
         "region_id": 1
      }
   ]

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
| labels   | body | string  | User defined labels                |
+----------+------+---------+------------------------------------+
| note     | body | string  | Note used for governance           |
+----------+------+---------+------------------------------------+


Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Cell Update
*******************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/cells/1" \
        -XPUT \
        -d '{"name": "changedName"}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

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
|          |      |         | - variables                   |
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
| variables| body | object  | User defined variables        |
+----------+------+---------+-------------------------------+

Examples Cell Update
********************

.. code-block:: json

   {
      "id": 1,
      "name": "changedName",
      "note": null,
      "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
      "region_id": 1
   }

Update Cell Variables
=====================

:PUT: /v1/cells/{id}/variables

Update user defined variables for the cell

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

Example Cell Update Variables
*****************************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/cells/1/variables" \
        -XPUT \
        -d '{"newKey": "sampleKey"}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| key    | body | string  | Identifier              |
+--------+------+---------+-------------------------+
| value  | body | object  | Data                    |
+--------+------+---------+-------------------------+

Example Cell Update Variables
*****************************

.. code-block:: json

   {
      "variables": 
      {
         "newKey": “sampleKey”
      }
   }

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

Delete Cell Variables
=====================

:DELETE: /v1/cells/{id}/variables

Delete existing key/value variables for the cell

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
