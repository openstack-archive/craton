.. _regions:

=======
Regions
=======

Definition of region

Create Region
=============

.. glossary::
    POST
        /v1/region

Creates a new Region

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| project_id| body | integer | ID of the project        |
+-----------+------+---------+--------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Create Region**

..literalinclude:: ../../doc/api_samples/regions/regions-create-req.json
   :language: javascript

Response
--------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| region    | body | object  | - id                     |
|           |      |         | - name                   |
|           |      |         | - project_id             |
|           |      |         | - cells                  |
|           |      |         | - note                   |
|           |      |         | - data                   |
+-----------+------+---------+--------------------------+
| region_id | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| project_id| body | integer | ID of the project        |
+-----------+------+---------+--------------------------+
| cells     | body | array   | array of cells           |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+

**Example Create Region**

..literalinclude:: ../../doc/api_samples/regions/regions-create-resp.json
   :language: javascript

List Regions
============

.. glossary::
    GET
        /v1/regions

Gets all Regions

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Default response: unexpected error

Request
-------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| name      | query| string  | Name of the region to get|
+-----------+------+---------+--------------------------+
| region_id | query| integer | ID of the region to get  |
+-----------+------+---------+--------------------------+

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
| regions   | body | array   | array of regions         |
+-----------+------+---------+--------------------------+
| region_id | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| project_id| body | integer | ID of the project        |
+-----------+------+---------+--------------------------+
| cells     | body | array   | array of cells           |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+

**Example List Regions** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-list-resp.json
   :language: javascript

**Example Unexpected Error** (TO-DO)

..literalinclude:: ../../doc/api_samples/errors/errors-unexpected-resp.json
   :language: javascript

Update Region
=============

.. glossary::
    PUT
        /v1/regions/{region_id}

Update an existing region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404), validation exception(405)

Request
-------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| region_id | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| project_id| body | integer | ID of the project        |
+-----------+------+---------+--------------------------+
| cells     | body | array   | array of cells           |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+
| region_id | path | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Update Region** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-update-req.json
   :language: javascript

Response
--------

+-----------+------+---------+--------------------------+
| Name      | In   | Type    | Description              |
+===========+======+=========+==========================+
| region    | body | object  | - id                     |
|           |      |         | - name                   |
|           |      |         | - project_id             |
|           |      |         | - cells                  |
|           |      |         | - note                   |
|           |      |         | - data                   |
+-----------+------+---------+--------------------------+
| region_id | body | integer | Unique ID of the region  |
+-----------+------+---------+--------------------------+
| name      | body | string  | Unique name of the region|
+-----------+------+---------+--------------------------+
| project_id| body | integer | ID of the project        |
+-----------+------+---------+--------------------------+
| cells     | body | array   | array of cells           |
+-----------+------+---------+--------------------------+
| note      | body | string  | Note used for governance |
+-----------+------+---------+--------------------------+
| data      | body | object  | User defined data        |
+-----------+------+---------+--------------------------+

**Example Update Region**  (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-update-resp.json
   :language: javascript

Update Region Data
==================

.. glossary::
    PUT
        /v1/regions/{region_id}/data

Update user defined data for the region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404), validation exception(405)

Request
-------

+----------+------+---------+-------------------------+
| Name     | In   | Type    | Description             |
+==========+======+=========+=========================+
| key      | body | string  | Identifier              |
+----------+------+---------+-------------------------+
| value    | body | object  | Data                    |
+----------+------+---------+-------------------------+
| region_id| path | integer | Unique ID of the region |
+----------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

**Example Update Region Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-upadate—data-req.json
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


**Example Update Region Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-update-data-resp.json
   :language: javascript

Delete Region
=============

.. glossary::
    DELETE
        /v1/regions/{region_id}

Deletes an existing record of a Region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404)

Request
-------

+----------+------+---------+-------------------------+
| Name     | In   | Type    | Description             |
+==========+======+=========+=========================+
| region_id| path | integer | Unique ID of the region |
+----------+------+---------+-------------------------+

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

.. glossary::
    DELETE
        /v1/regions/{region_id}/data

Delete existing key/value data for the region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404) validation exception(405)

Request
-------

+----------+------+---------+-------------------------+
| Name     | In   | Type    | Description             |
+==========+======+=========+=========================+
| region_id| path | integer | Unique ID of the region |
+----------+------+---------+-------------------------+

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: application/json
    - X-Auth-Token
    - X-Auth-User
    - X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
