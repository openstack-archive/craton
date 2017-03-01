.. _regions:

=======
Regions
=======

Definition of region

Create Region
=============

:POST: /v1/region

Creates a new Region

Normal response codes: OK(201)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+----------+------+---------+--------------------------+
| Name     | In   | Type    | Description              |
+==========+======+=========+==========================+
| name     | body | string  | Unique name of the region|
+----------+------+---------+--------------------------+
| labels   | body | string  | User defined labels      |
+----------+------+---------+--------------------------+
| note     | body | string  | Note used for governance |
+----------+------+---------+--------------------------+
| variables| body | object  | User defined variables   |
+----------+------+---------+--------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Region Create
*********************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/regions" \
        -d '{"name": "DFW"}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"   

Response
--------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| region    | body | object  | - id                     |
|           |      |         | - name                   |
|           |      |         | - cells                  |
|           |      |         | - labels                 |
|           |      |         | - note                   |
|           |      |         | - variables              |
+-----------+------+---------+--------------------------+
| id        | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| cells     | body | array   | Array of cells           |
+-----------+------+---------+--------------------------+
| labels    | body | string  | User defined labels      |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| variables | body | object  | User defined variables   |
+-----------+------+---------+--------------------------+

Example Region Create 
*********************

.. code-block:: json

   {
      "id": 1,
      "name": "DFW",
      "note": null
   }

List Regions
============

:GET: /v1/regions

Gets all Regions

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Default response: unexpected error

Request
-------
No parameters 

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Region List
*******************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/regions" \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| regions   | body | array   | Array of regions         |
+-----------+------+---------+--------------------------+
| id        | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| cells     | body | array   | Array of cells in region |
+-----------+------+---------+--------------------------+
| labels    | body | string  | User defined labels      |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| variables | body | object  | User defined variables   |
+-----------+------+---------+--------------------------+

Example Region List
*******************

.. code-block:: bash

   [
      {
         "id": 1,
         "name": "DFW",
         "note": null
      }, 
      {
         "id": 2, 
         "name": "DFW2",
         "note": null
      }, 
      {
         "id": 3,
         "name": "fooRegion",
         "note": null
      }
   ]

.. todo:: **Example Unexpected Error**

 ..literalinclude:: ./api_samples/errors/errors-unexpected-resp.json
    :language: javascript

Update Region
=============

:PUT: /v1/regions/{id}

Update an existing region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404), validation exception(405)

Request
-------

+-----------+------+---------+--------------------------------------+
| Name      | In   | Type    | Description                          |
+===========+======+=========+======================================+
| name      | body | string  | Unique name of the region            |
+-----------+------+---------+--------------------------------------+
| cells     | body | array   | Array of cells in region             |
+-----------+------+---------+--------------------------------------+
| labels    | body | string  | User defined labels                  |
+-----------+------+---------+--------------------------------------+
| note      | body | string  | Note used for governance             |
+-----------+------+---------+--------------------------------------+
| id        | path | integer | Unique ID of the region to be updated|
+-----------+------+---------+--------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Region Update
*********************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/regions/3" \
        -XPUT \
        -d '{"name": "DFW3"}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| region    | body | object  | - id                     |
|           |      |         | - name                   |
|           |      |         | - cells                  |
|           |      |         | - labels                 |
|           |      |         | - note                   |
|           |      |         | - variables              |
+-----------+------+---------+--------------------------+
| id        | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| cells     | body | array   | Array of cells in region |
+-----------+------+---------+--------------------------+
| labels    | body | string  | User defined labels      |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| variables | body | object  | User defined variables   |
+-----------+------+---------+--------------------------+

Example Region Update
*********************

.. code-block:: json

   {
      "id": 3,
      "name": "DFW3",
      "note": null,
      "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06"
   }

Update Region Variables
=======================

:PUT: /v1/regions/{id}/variables

Update user defined variables for the region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404), validation exception(405)

Request
-------

+----------+------+---------+--------------------------------------+
| Name     | In   | Type    | Description                          |
+==========+======+=========+======================================+
| key      | body | string  | Identifier                           |
+----------+------+---------+--------------------------------------+
| value    | body | object  | Data                                 |
+----------+------+---------+--------------------------------------+
| id       | path | integer | Unique ID of the region to be updated|
+----------+------+---------+--------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Region Variables Update
*******************************

.. code-block:: bash

   curl -i "http://${MY_IP}:7780/v1/regions/3/variables" \
        -XPUT \
        -d '{“array”: [2]}' \
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

Example Region Variables Update
*******************************

.. code-block:: json

   {
      "variables": 
      {
         "string": "sample text",
         "value": 24,
         "array": [2]
      }
   }

Delete Region
=============

:DELETE: /v1/regions/{id}

Deletes an existing record of a Region

Normal response codes: no content(204)

Error response codes: invalid request(400), region not found(404)

Request
-------

+------+------+---------+--------------------------------------+
| Name | In   | Type    | Description                          |
+======+======+=========+======================================+
| id   | path | integer | Unique ID of the region to be deleted|
+------+------+---------+--------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: applicaton/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Region Variables
=======================

:DELETE: /v1/regions/{id}/variables

Delete existing key/value variables for the region

Normal response codes: no content(204)

Error response codes: invalid request(400), region not found(404) validation exception(405)

Request
-------

+-------+------+---------+-------------------------+
| Name  | In   | Type    | Description             |
+=======+======+=========+=========================+
| id    | path | integer | Unique ID of the region |
+-------+------+---------+-------------------------+
| key   | body | string  | Identifier to be deleted|
+-------+------+---------+-------------------------+
| value | body | object  | Data to be deleted      |
+-------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
