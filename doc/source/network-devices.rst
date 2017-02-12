.. _network-devices:

==============
Network Device
==============

Definition of network device

Create Network Device
=====================

:POST: /v1/network-devices

Create a new network device

Normal response codes: created(201)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+-----------------+------+---------+-------------------------------------------------+
| Name            | In   | Type    | Description                                     |
+=================+======+=========+=================================================+
| created_at      | body | string  | Timestamp of network device creation            |
+-----------------+------+---------+-------------------------------------------------+
| updated_at      | body | string  | Timestamp of last network device update         |
+-----------------+------+---------+-------------------------------------------------+
| hostname        | body | string  | Name of the host of the device                  |
+-----------------+------+---------+-------------------------------------------------+
| id              | body | integer | Unique ID of the network device                 |
+-----------------+------+---------+-------------------------------------------------+
| cell_id         | body | integer | Unique ID of the network device's cell          |
+-----------------+------+---------+-------------------------------------------------+
| region_id       | body | integer | Unique ID of the network device's region        |
+-----------------+------+---------+-------------------------------------------------+
| parent_id       | body | integer | ID of the network device's parent               |
+-----------------+------+---------+-------------------------------------------------+
| ip_address      | body | string  | IP address of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| device_type     | body | string  | Type of device                                  |
+-----------------+------+---------+-------------------------------------------------+
| model_name      | body | string  | Model name of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| os_version      | body | string  | Operating system version of the network device  |
+-----------------+------+---------+-------------------------------------------------+
| vlans           | body | string  | virtual local area networks of the device       |
+-----------------+------+---------+-------------------------------------------------+
| interface_id    | body | integer | Unique ID of the interface of the device        |
+-----------------+------+---------+-------------------------------------------------+
| network_id      | body | integer | Unique ID of the network of the device          |
+-----------------+------+---------+-------------------------------------------------+
| active          | body | boolean | State of the network device                     |
+-----------------+------+---------+-------------------------------------------------+
| labels          | body | string  | User defined labels                             |
+-----------------+------+---------+-------------------------------------------------+
| note            | body | string  | Note used for governance                        |
+-----------------+------+---------+-------------------------------------------------+
| variables       | body | object  | User defined variables                          |
+-----------------+------+---------+-------------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Device Create
*****************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-devices" \
      -d '{"hostname": "fooHost", "region_id": 1, "ip_address": "1.1.1.4", "device_type": "NIC"}' \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-----------------+------+---------+-------------------------------------------------+
| Name            | In   | Type    | Description                                     |
+=================+======+=========+=================================================+
| network-device  | body | object  | - created_at                                    |
|                 |      |         | - updated_at                                    |
|                 |      |         | - hostname                                      |
|                 |      |         | - id                                            |
|                 |      |         | - cell_id                                       |
|                 |      |         | - region_id                                     |
|                 |      |         | - parent_id                                     |
|                 |      |         | - ip_address                                    |
|                 |      |         | - device_type                                   |
|                 |      |         | - model_name                                    |
|                 |      |         | - os_version                                    |
|                 |      |         | - vlans                                         |
|                 |      |         | - interface_id                                  |
|                 |      |         | - network_id                                    |
|                 |      |         | - active                                        |
|                 |      |         | - labels                                        |
|                 |      |         | - note                                          |
|                 |      |         | - variables                                     |
+-----------------+------+---------+-------------------------------------------------+
| created_at      | body | string  | Timestamp of network device creation            |
+-----------------+------+---------+-------------------------------------------------+
| updated_at      | body | string  | Timestamp of last network device update         |
+-----------------+------+---------+-------------------------------------------------+
| hostname        | body | string  | Name of the host of the device                  |
+-----------------+------+---------+-------------------------------------------------+
| id              | body | integer | Unique ID of the network device                 |
+-----------------+------+---------+-------------------------------------------------+
| cell_id         | body | integer | Unique ID of the network device's cell          |
+-----------------+------+---------+-------------------------------------------------+
| region_id       | body | integer | Unique ID of the network device's region        |
+-----------------+------+---------+-------------------------------------------------+
| parent_id       | body | integer | ID of the network device's parent               |
+-----------------+------+---------+-------------------------------------------------+
| ip_address      | body | string  | IP address of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| device_type     | body | string  | Type of device                                  |
+-----------------+------+---------+-------------------------------------------------+
| model_name      | body | string  | Model name of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| os_version      | body | string  | Operating system version of the network device  |
+-----------------+------+---------+-------------------------------------------------+
| vlans           | body | string  | virtual local area networks of the device       |
+-----------------+------+---------+-------------------------------------------------+
| interface_id    | body | integer | Unique ID of the interface of the device        |
+-----------------+------+---------+-------------------------------------------------+
| network_id      | body | integer | Unique ID of the network of the device          |
+-----------------+------+---------+-------------------------------------------------+
| active          | body | boolean | State of the network device                     |
+-----------------+------+---------+-------------------------------------------------+
| labels          | body | string  | User defined labels                             |
+-----------------+------+---------+-------------------------------------------------+
| note            | body | string  | Note used for governance                        |
+-----------------+------+---------+-------------------------------------------------+
| variables       | body | object  | User defined variables                          |
+-----------------+------+---------+-------------------------------------------------+

Example Network Device Create
*****************************

.. code-block:: json

   {
      "cell_id": null,
      "device_type": "NIC",
      "id": 6,
      "ip_address": "1.1.1.4",
      "model_name": null,
      "os_version": null,
      "parent_id": null,
      "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
      "region_id": 1,
      "vlans": null
   }

List Network Device
===================

:GET: /v1/network-devices?region_id=

Gets all network devices in a region

Normal response codes: OK(200)

Error response codes: invalid request(400), device not found(404), validation exception(405)

Default response: unexpected error

Request
-------

+------------+------+---------+---------+--------------------------------+
| Name       | In   | Type    | Required| Description                    |
+============+======+=========+=========+================================+
| region_id  | query| integer | Yes     | ID of the region to get device |
+------------+------+---------+---------+--------------------------------+
| id         | query| integer | No      | ID of the network device to get|
+------------+------+---------+---------+--------------------------------+
| name       | query| string  | No      | Name of the device to get      |
+------------+------+---------+---------+--------------------------------+
| cell_id    | query| integer | No      | Name of the cell to get        |
+------------+------+---------+---------+--------------------------------+
| ip_address | query| string  | No      | IP address of the host to get  |
+------------+------+---------+---------+--------------------------------+
| device_type| query| string  | No      | Type of host to get            |
+------------+------+---------+---------+--------------------------------+
| vars       | query| string  | No      | Variable filters to get device |
+------------+------+---------+---------+--------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Device List
***************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-devices?region_id=1" \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-----------------+------+---------+-------------------------------------------------+
| Name            | In   | Type    | Description                                     |
+=================+======+=========+=================================================+
| network-device  | body | array   | array of network device                         |
+-----------------+------+---------+-------------------------------------------------+
| created_at      | body | string  | Timestamp of network device creation            |
+-----------------+------+---------+-------------------------------------------------+
| updated_at      | body | string  | Timestamp of last network device update         |
+-----------------+------+---------+-------------------------------------------------+
| hostname        | body | string  | Name of the host of the device                  |
+-----------------+------+---------+-------------------------------------------------+
| id              | body | integer | Unique ID of the network device                 |
+-----------------+------+---------+-------------------------------------------------+
| cell_id         | body | integer | Unique ID of the network device's cell          |
+-----------------+------+---------+-------------------------------------------------+
| region_id       | body | integer | Unique ID of the network device's region        |
+-----------------+------+---------+-------------------------------------------------+
| parent_id       | body | integer | ID of the network device's parent               |
+-----------------+------+---------+-------------------------------------------------+
| ip_address      | body | string  | IP address of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| device_type     | body | string  | Type of device                                  |
+-----------------+------+---------+-------------------------------------------------+
| model_name      | body | string  | Model name of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| os_version      | body | string  | Operating system version of the network device  |
+-----------------+------+---------+-------------------------------------------------+
| vlans           | body | string  | virtual local area networks of the device       |
+-----------------+------+---------+-------------------------------------------------+
| interface_id    | body | integer | Unique ID of the interface of the device        |
+-----------------+------+---------+-------------------------------------------------+
| network_id      | body | integer | Unique ID of the network of the device          |
+-----------------+------+---------+-------------------------------------------------+
| active          | body | boolean | State of the network device                     |
+-----------------+------+---------+-------------------------------------------------+
| labels          | body | string  | User defined labels                             |
+-----------------+------+---------+-------------------------------------------------+
| note            | body | string  | Note used for governance                        |
+-----------------+------+---------+-------------------------------------------------+
| variables       | body | object  | User defined variables                          |
+-----------------+------+---------+-------------------------------------------------+

Example Network Device List
***************************

.. code-block:: json

   [
      {
         "cell_id": null,
         "device_type": "NIC",
         "id": 6,
         "ip_address": "1.1.1.4",
         "model_name": null,
         "os_version": null,
         "parent_id": null,
         "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
         "region_id": 1,
         "vlans": null
      },
      {
         "cell_id": null,
         "device_type": "Bridge",
         "id": 8,
         "ip_address": "1.1.1.8",
         "model_name": null,
         "os_version": null,
         "parent_id": null,
         "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
         "region_id": 1,
         "vlans": null
      }
   ]

.. todo:: **Example Unexpected Error**

 ..literalinclude:: ./api_samples/errors/errors-unexpected-resp.json
    :language: javascript

Update Network Device
=====================

:PUT: /v1/network-devices/{id}

Update an existing network device

Normal response codes: OK(200)

Error response codes: invalid request(400), device not found(404), validation exception(405)

Request
-------

+-----------------+------+---------+-------------------------------------------------+
| Name            | In   | Type    | Description                                     |
+=================+======+=========+=================================================+
| hostname        | body | string  | Name of the host of the device                  |
+-----------------+------+---------+-------------------------------------------------+
| ip_address      | body | string  | IP address of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| device_type     | body | string  | Type of device                                  |
+-----------------+------+---------+-------------------------------------------------+
| model_name      | body | string  | Model name of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| os_version      | body | string  | Operating system version of the network device  |
+-----------------+------+---------+-------------------------------------------------+
| vlans           | body | string  | virtual local area networks of the device       |
+-----------------+------+---------+-------------------------------------------------+
| active          | body | boolean | State of the network device                     |
+-----------------+------+---------+-------------------------------------------------+
| labels          | body | string  | User defined labels                             |
+-----------------+------+---------+-------------------------------------------------+
| note            | body | string  | Note used for governance                        |
+-----------------+------+---------+-------------------------------------------------+

Example Network Device Update
*****************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-devices/6" \
      -XPUT \
      -d '{"hostname": "newHostName", "ip_address": "0.0.0.0"}' \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-----------------+------+---------+-------------------------------------------------+
| Name            | In   | Type    | Description                                     |
+=================+======+=========+=================================================+
| created_at      | body | string  | Timestamp of network device creation            |
+-----------------+------+---------+-------------------------------------------------+
| updated_at      | body | string  | Timestamp of last network device update         |
+-----------------+------+---------+-------------------------------------------------+
| hostname        | body | string  | Name of the host of the device                  |
+-----------------+------+---------+-------------------------------------------------+
| id              | body | integer | Unique ID of the network device                 |
+-----------------+------+---------+-------------------------------------------------+
| cell_id         | body | integer | Unique ID of the network device's cell          |
+-----------------+------+---------+-------------------------------------------------+
| region_id       | body | integer | Unique ID of the network device's region        |
+-----------------+------+---------+-------------------------------------------------+
| parent_id       | body | integer | ID of the network device's parent               |
+-----------------+------+---------+-------------------------------------------------+
| ip_address      | body | string  | IP address of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| device_type     | body | string  | Type of device                                  |
+-----------------+------+---------+-------------------------------------------------+
| model_name      | body | string  | Model name of the network device                |
+-----------------+------+---------+-------------------------------------------------+
| os_version      | body | string  | Operating system version of the network device  |
+-----------------+------+---------+-------------------------------------------------+
| vlans           | body | string  | virtual local area networks of the device       |
+-----------------+------+---------+-------------------------------------------------+
| interface_id    | body | integer | Unique ID of the interface of the device        |
+-----------------+------+---------+-------------------------------------------------+
| network_id      | body | integer | Unique ID of the network of the device          |
+-----------------+------+---------+-------------------------------------------------+
| active          | body | boolean | State of the network device                     |
+-----------------+------+---------+-------------------------------------------------+
| labels          | body | string  | User defined labels                             |
+-----------------+------+---------+-------------------------------------------------+
| note            | body | string  | Note used for governance                        |
+-----------------+------+---------+-------------------------------------------------+
| variables       | body | object  | User defined variables                          |
+-----------------+------+---------+-------------------------------------------------+

Example Network Device Update
*****************************

.. code-block:: json

   {
      "cell_id": null,
      "device_type": "NIC",
      "id": 6,
      "ip_address": "0.0.0.0",
      "model_name": null,
      "os_version": null,
      "parent_id": null,
      "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
      "region_id": 1,
      "vlans": null
   }

Update Network Device Variables
===============================

:PUT: /v1/network-devices/{id}/variables

Update user defined variables for the network device

Normal response codes: OK(200)

Error response codes: invalid request(400), device not found(404), validation exception(405)

Request
-------

+--------+------+---------+----------------------------------------------+
| Name   | In   | Type    | Description                                  |
+========+======+=========+==============================================+
| key    | body | string  | Identifier                                   |
+--------+------+---------+----------------------------------------------+
| value  | body | object  | Data                                         |
+--------+------+---------+----------------------------------------------+
| id     | path | integer | Unique ID of the network device to be updated|
+--------+------+---------+----------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Device Variables Update
***************************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-devices/6/variables" \
      -XPUT \
      -d '{"newVar": "sample variable"}' \
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

Example Network Device Variables Update
***************************************

.. code-block:: json

   {
      "variables":
       {
          "newVar": "sample variable"
       }
   }

Delete Network Device
=====================

:DELETE: /v1/network-devices/{id}

Deletes an existing record of a network device

Normal response codes: no content(204)

Error response codes: invalid request(400), device not found(404)

Request
-------

+--------+------+---------+----------------------------------------------+
| Name   | In   | Type    | Description                                  |
+========+======+=========+==============================================+
| id     | path | integer | Unique ID of the network device to be deleted|
+--------+------+---------+----------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Network Device Variables
===============================

:DELETE: /v1/network-devices/{id}/variables

Delete existing key/value variables for the network device

Normal response codes: no content(204)

Error response codes: invalid request(400), device not found(404) validation exception(405)

Request
-------

+--------+------+---------+--------------------------------+
| Name   | In   | Type    | Description                    |
+========+======+=========+================================+
| id     | path | integer | Unique ID of the network device|
+--------+------+---------+--------------------------------+
| key    | body | string  | Identifier to be deleted       |
+--------+------+---------+--------------------------------+
| value  | body | object  | Data to be deleted             |
+--------+------+---------+--------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
