.. -*- rst -*-

=======
Regions
=======

Definition of region

Create Region
==============

.. rest_method:: POST /v1/region

Creates a new Region

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - name: region_name
    - project_id: project_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Create Region**

..literalinclude:: ../../doc/api_samples/regions/regions-create-req.json
   :language: javascript

Response
--------

    - region: region
    - id: region_id_body
    - name: region_name
    - project_id: project_id
    - cells: cells
    - data: data

**Example Create Region**

..literalinclude:: ../../doc/api_samples/regions/regions-create-resp.json
   :language: javascript

List Regions
==============

.. rest_method::  GET /v1/regions

Gets all Regions

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Default response: unexpected error

Request
--------

    - name: region_name_query
    - id: region_id_query

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

.. rest_parameters:: parameters.yaml

    - region: region
    - id: region_id_body
    - name: region_name
    - project_id: project_id
    - cells: cells
    - data: data

**Example List Regions**

..literalinclude:: ../../doc/api_samples/regions/regions-list-resp.json
   :language: javascript

**Example Unexpected Error **

..literalinclude:: ../../doc/api_samples/errors/errors-unexpected-resp.json
   :language: javascript

Update Region
=============

.. rest_method:: PUT /v1/regions/{region_id}

Update an existing region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - id: region_id_body
    - name: region_name
    - project_id: project_id
    - cells: cells
    - data: data
    - region_id: region_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Update Region** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-update-req.json
   :language: javascript

Response
--------

    - region: region
    - id: region_id_body
    - name: region_name
    - project_id: project_id
    - cells: cells
    - data: data

**Example Update Region**  (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-update-resp.json
   :language: javascript

Update Region Data
==================

.. rest_method:: PUT /v1/regions/{region_id}/data

Update user defined data for the region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - key: key
    - value: value
    - region_id: region_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Update Region Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-upadate—data-req.json
   :language: javascript

Response
--------

    - key: key
    - value: value

**Example Update Region Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/regions/regions-update-data-resp.json
   :language: javascript

Delete Region
==============

.. rest_method:: DELETE /v1/regions/{region_id}

Deletes an existing record of a Region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404)

Request
-------

.. rest_parameters:: parameters.yaml

    - region_id: region_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Region Data
==================

.. rest_method:: DELETE /v1/regions/{region_id}/data

Delete existing key/value data for the region

Normal response codes: OK(200)

Error response codes: invalid request(400), region not found(404) validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - region_id: region_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
