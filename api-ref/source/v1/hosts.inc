.. -*- rst -*-

=====
Hosts
=====

Definition of host

Create Host
============

.. rest_method:: POST /v1/hosts

Create a new host

Normal response codes: OK(201)

Error response codes: invalid request(400), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - name: host_name
    - region_id: region_id_body
    - project_id: project_id
    - ip_address: ip_address
    - device_type: device_type

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Create Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-create-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

    - host: host
    - id: host_id_body
    - name: host_name
    - cell_id: cell_id_body
    - parent_id: parent_id
    - project_id: project_id
    - region_id: region_id_body
    - ip_address: ip_address
    - device_type: device_type
    - labels: labels
    - note: note
    - variables: variables

**Example Create Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-create-resp.json
   :language: javascript

List Hosts
==========

.. rest_method::  GET /v1/hosts

Gets all Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Default response: unexpected error

Request
--------

.. rest_parameters:: parameters.yaml

    - limit: limit
    - name: host_name_query
    - id: host_id_query
    - region: region_name_query
    - cell: cell_name_query
    - ip_address: ip_address_query
    - service: service

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

.. rest_parameters:: parameters.yaml

    - hosts: hosts
    - id: host_id_body
    - name: host_name
    - cell_id: cell_id_body
    - parent_id: parent_id
    - project_id: project_id
    - region_id: region_id_body
    - ip_address: ip_address
    - device_type: device_type
    - labels: labels
    - note: note
    - variables: variables

**Example List Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-list-resp.json
   :language: javascript

**Example Unexpected Error **

..literalinclude:: ../../doc/api_samples/errors/errors-unexpected-resp.json
   :language: javascript

Update Hosts
============

.. rest_method:: PUT /v1/hosts/{host_id}

Update an existing host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - id: host_id_body
    - name: host_name
    - cell_id: cell_id_body
    - parent_id: parent_id
    - project_id: project_id
    - region_id: region_id_body
    - ip_address: ip_address
    - device_type: device_type
    - labels: labels
    - note: note
    - variables: variables
    - host_id: host_id


Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Update Host** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-update-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

    - host: host
    - id: host_id_body
    - name: host_name
    - cell_id: cell_id_body
    - parent_id: parent_id
    - project_id: project_id
    - region_id: region_id_body
    - ip_address: ip_address
    - device_type: device_type
    - labels: labels
    - note: note
    - variables: variables

**Example Update Host**  (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-update-resp.json
   :language: javascript

Update Host Data
==================

.. rest_method:: PUT /v1/hosts/{host_id}/variables

Update user defined variables for the host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - key: key
    - value: value
    - host_id: host_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

**Example Update Host Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-upadate—data-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

    - key: key
    - value: value

**Example Update Host Data** (TO-DO)

..literalinclude:: ../../doc/api_samples/hosts/hosts-update-data-resp.json
   :language: javascript

Delete Host
===========

.. rest_method:: DELETE /v1/hosts/{host_id}

Deletes an existing record of a Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404)

Request
-------

.. rest_parameters:: parameters.yaml

    - host_id: host_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Host Data
================

.. rest_method:: DELETE /v1/hosts/{host_id}/variables

Delete existing key/value variables for the Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404) validation exception(405)

Request
-------

.. rest_parameters:: parameters.yaml

    - host_id: host_id

Required Header
^^^^^^^^^^^^^^^

    - Content-Type: Content_Type
    - X-Auth-Token: X-Auth-Token
    - X-Auth-User: X-Auth-User
    - X-Auth-Project: X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
