.. -*- rst -*-
======
Cells
======

Definition of cell

Create Cell
============

.. rest_method:: POST /v1/cells

Create a new Cell

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - name : cell_name
    - region_id: region_id_body
    - project_id: project_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Create Cell** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-create-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

    - cell: cell
    - id: cell_id_body
    - name: cell_name
    - region_id: region_id_body
    - project_id: project_id
    - note: note
    - variables: variables

**Example Create Cell** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-create-resp.json
   :language: javascript

List Cells
==========

.. rest_method::  GET /v1/cells

Gets all Cells

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Default response: unexpected error

Request
--------

.. rest_parameters:: parameters.yaml

    - cell: cell_name_query
    - region: region_name_query

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

.. rest_parameters:: parameters.yaml

    - cells: cells
    - id: cell_id_body
    - name: cell_name
    - region_id: region_id_body
    - project_id: project_id
    - note: note
    - variables: variables

**Example List Cells** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-list-resp.json
   :language: javascript

**Example Unexpected Error **

..literalinclude:: ../../doc/api_samples/errors/errors-unexpected-resp.json
   :language: javascript

Update Cells
============

.. rest_method:: PUT /v1/cells/{cell_id}

Update an existing cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - id: cell_id_body
    - name: cell_name
    - region_id: region_id_body
    - project_id: project_id
    - note: note
    - variables: variables
    - cell_id: cell_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Update Cell** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-update-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

    - cell: cell
    - id: cell_id_body
    - name: cell_name
    - region_id: region_id_body
    - project_id: project_id
    - note: note
    - variables: variables

**Example Update Cell**  (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-update-resp.json
   :language: javascript

Update Cell Data
==================

.. rest_method:: PUT /v1/cells/{cell_id}/variables

Update user defined variables for the cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - key: key
    - value: value
    - cell_id: cell_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Update Cell Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-upadate—data-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

    - key: key
    - value: value

**Example Update Cell Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/cells/cells-update-data-resp.json
   :language: javascript

Delete Cell
===========

.. rest_method:: DELETE /v1/cells/{cell_id}

Deletes an existing record of a Cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404)

Request
-------

.. rest_parameters:: parameters.yaml

    - cell_id: cell_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Cell Data
================

.. rest_method:: DELETE /v1/cells/{cell_id}/variables

Delete existing key/value variable for the cell

Normal response codes: OK(200)

Error response codes: invalid request(400), cell not found(404) validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - cell_id: cell_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
