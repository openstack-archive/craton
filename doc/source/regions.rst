.. _regions:

=======
Regions
=======

Definition of region

Create Region
=============

:POST: /v1/region

Creates a new Region

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+-------+------+---------+--------------------------+
| Name  | In   | Type    | Description              |
+=======+======+=========+==========================+
| name  | body | string  | Unique name of the region|
+-------+------+---------+--------------------------+
| labels| body | string  | User defined labels      |
+-------+------+---------+--------------------------+
| note  | body | string  | Note used for governance |
+-------+------+---------+--------------------------+
| data  | body | object  | User defined data        |
+-------+------+---------+--------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Create Region**

 ..literalinclude:: ./api_samples/regions/regions-create-req.json
    :language: javascript

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
|           |      |         | - data                   |
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
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+

.. todo:: **Example Create Region**

 ..literalinclude:: ./api_samples/regions/regions-create-resp.json
    :language: javascript

List Regions
============

:GET: /v1/regions

Gets all Regions

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Default response: unexpected error

Request
-------

+-----+------+---------+---------+--------------------------+
| Name| In   | Type    | Required| Description              |
+=====+======+=========+=========+==========================+
| id  | query| integer | No      | ID of the region to get  |
+-----+------+---------+---------+--------------------------+
| name| query| string  | No      | Name of the region to get|
+-----+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

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
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+

.. todo:: **Example List Regions**

 ..literalinclude:: ./api_samples/regions/regions-list-resp.json
    :language: javascript

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
| data      | body | object  | User defined data                    |
+-----------+------+---------+--------------------------------------+
| id        | path | integer | Unique ID of the region to be updated|
+-----------+------+---------+--------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

.. todo:: **Example Update Region**

 ..literalinclude:: ./api_samples/regions/regions-update-req.json
    :language: javascript

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
|           |      |         | - data                   |
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
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+

.. todo:: **Example Update Region**

 ..literalinclude:: ./api_samples/regions/regions-update-resp.json
    :language: javascript

Update Region Data
==================

:PUT: /v1/regions/{id}/data

Update user defined data for the region	

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

.. todo:: **Example Update Region Data**

 ..literalinclude:: ./api_samples/regions/regions-upadate—data-req.json
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


.. todo:: **Example Update Region Data**

 ..literalinclude:: ./api_samples/regions/regions-update-data-resp.json
    :language: javascript

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

Delete Region Data
==================

:DELETE: /v1/regions/{id}/data

Delete existing key/value data for the region

Normal response codes: no content(204)

Error response codes: invalid request(400), region not found(404) validation exception(405)

Request
-------

+------+------+---------+--------------------------------------+
| Name | In   | Type    | Description                          |
+======+======+=========+======================================+
| id   | path | integer | Unique ID of the region to be deleted|
+------+------+---------+--------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
