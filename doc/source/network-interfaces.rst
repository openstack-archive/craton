.. _network-interfaces:

=================
Network Interface
=================

Definition of network interface

Create Network Interface
========================

:POST: /v1/network-interfaces

Create a new network interface

Normal response codes: created(201)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+-----------------+------+---------+-------------------------------------------------+
| Name            | In   | Type    | Description                                     |
+=================+======+=========+=================================================+
| created_at      | body | string  | Timestamp of network interface creation         |
+-----------------+------+---------+-------------------------------------------------+
| updated_at      | body | string  | Timestamp of last network interface update      |
+-----------------+------+---------+-------------------------------------------------+
| name            | body | string  | Name of the interface                           |
+-----------------+------+---------+-------------------------------------------------+
| id              | body | integer | Unique ID of the network interface              |
+-----------------+------+---------+-------------------------------------------------+
| device_id       | body | integer | Unique ID of the interface's device             |
+-----------------+------+---------+-------------------------------------------------+
| network_id      | body | integer | Unique ID of the interfaces's netowrk           |
+-----------------+------+---------+-------------------------------------------------+
| interface_type  | body | string  | Type of network interface                       |
+-----------------+------+---------+-------------------------------------------------+
| project_id      | body | string  | ID of the network interface's project           |
+-----------------+------+---------+-------------------------------------------------+
| vlan_id         | body | integer | ID of the VLAN of the network interface         |
+-----------------+------+---------+-------------------------------------------------+
| vlan            | body | string  | virtual local area netowrk of the interface     |
+-----------------+------+---------+-------------------------------------------------+
| port            | body | integer | Number of the port of the network interface     |
+-----------------+------+---------+-------------------------------------------------+
| duplex          | body | string  | Operation type of network interface             |
+-----------------+------+---------+-------------------------------------------------+
| speed           | body | integer | Bandwidth of the netork interface               |
+-----------------+------+---------+-------------------------------------------------+
| link            | body | string  | Channel between network interfaces              |
+-----------------+------+---------+-------------------------------------------------+
| cdp             | body | string  | Cisco Discovery Protocol                        |
+-----------------+------+---------+-------------------------------------------------+
| security        | body | string  | Security protocol of the network interface      |
+-----------------+------+---------+-------------------------------------------------+
| ip_address      | body | string  | Internet protocol address of the interface      |
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

Example Network Interface Create
********************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-interfaces" \
      -d '{"name": "myNetInterface", "device_id": 1, "interface_type": "ethernet", "ip_address": "10.10.0.1"}' \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-------------------+------+---------+-------------------------------------------------+
| Name              | In   | Type    | Description                                     |
+===================+======+=========+=================================================+
| network-interface | body | object  | - created_at                                    |
|                   |      |         | - updated_at                                    |
|                   |      |         | - name                                          |
|                   |      |         | - id                                            |
|                   |      |         | - device_id                                     |
|                   |      |         | - network_id                                    |
|                   |      |         | - interface_type                                |
|                   |      |         | - project_id                                    |
|                   |      |         | - vlan_id                                       |
|                   |      |         | - vlan                                          |
|                   |      |         | - port                                          |
|                   |      |         | - duplex                                        |
|                   |      |         | - speed                                         |
|                   |      |         | - link                                          |
|                   |      |         | - cdp                                           |
|                   |      |         | - security                                      |
|                   |      |         | - ip_address                                    |
|                   |      |         | - labels                                        |
|                   |      |         | - note                                          |
|                   |      |         | - variables                                     |
+-------------------+------+---------+-------------------------------------------------+
| created_at        | body | string  | Timestamp of network interface creation         |
+-------------------+------+---------+-------------------------------------------------+
| updated_at        | body | string  | Timestamp of last network interface update      |
+-------------------+------+---------+-------------------------------------------------+
| name              | body | string  | Name of the interface                           |
+-------------------+------+---------+-------------------------------------------------+
| id                | body | integer | Unique ID of the network interface              |
+-------------------+------+---------+-------------------------------------------------+
| device_id         | body | integer | Unique ID of the interface's device             |
+-------------------+------+---------+-------------------------------------------------+
| network_id        | body | integer | Unique ID of the interfaces's netowrk           |
+-------------------+------+---------+-------------------------------------------------+
| interface_type    | body | string  | Type of network interface                       |
+-------------------+------+---------+-------------------------------------------------+
| project_id        | body | string  | ID of the network interface's project           |
+-------------------+------+---------+-------------------------------------------------+
| vlan_id           | body | integer | ID of the VLAN of the network interface         |
+-------------------+------+---------+-------------------------------------------------+
| vlan              | body | string  | virtual local area netowrk of the interface     |
+-------------------+------+---------+-------------------------------------------------+
| port              | body | integer | Number of the port of the network interface     |
+-------------------+------+---------+-------------------------------------------------+
| duplex            | body | string  | Operation type of network interface             |
+-------------------+------+---------+-------------------------------------------------+
| speed             | body | integer | Bandwidth of the netork interface               |
+-------------------+------+---------+-------------------------------------------------+
| link              | body | string  | Channel between network interfaces              |
+-------------------+------+---------+-------------------------------------------------+
| cdp               | body | string  | Cisco Discovery Protocol                        |
+-------------------+------+---------+-------------------------------------------------+
| security          | body | string  | Security protocol of the network interface      |
+-------------------+------+---------+-------------------------------------------------+
| ip_address        | body | string  | Internet protocol address of the interface      |
+-------------------+------+---------+-------------------------------------------------+
| labels            | body | string  | User defined labels                             |
+-------------------+------+---------+-------------------------------------------------+
| note              | body | string  | Note used for governance                        |
+-------------------+------+---------+-------------------------------------------------+
| variables         | body | object  | User defined variables                          |
+-------------------+------+---------+-------------------------------------------------+

Example Network Interface Create
********************************

.. code-block:: json

   {
      "cdp": null,
      "device_id": 1,
      "duplex": null,
      "id": 1,
      "interface_type": "ethernet",
      "ip_address": "10.10.0.1",
      "link": null,
      "name": "myNetInterface",
      "network_id": null,
      "port": null,
      "project_id": "717e9a216e2d44e0bc848398563bda06",
      "security": null,
      "speed": null,
      "vlan": null,
      "vlan_id": null
   }

List Network Interface
======================

:GET: /v1/network-interfaces

Gets all network interfaces

Normal response codes: OK(200)

Error response codes: invalid request(400), interface not found(404), validation exception(405)

Default response: unexpected error

Request
-------

+----------------+------+---------+---------+------------------------------------------+
| Name           | In   | Type    | Required| Description                              |
+================+======+=========+=========+==========================================+
| id             | query| integer | No      | ID of the net interface to get           |
+----------------+------+---------+---------+------------------------------------------+
| device_id      | query| integer | No      | Device ID of the interface to get        |
+----------------+------+---------+---------+------------------------------------------+
| ip_address     | query| string  | No      | IP of the interface to get               |
+----------------+------+---------+---------+------------------------------------------+
| interface_type | query| string  | No      | Type of the interface to get             |
+----------------+------+---------+---------+------------------------------------------+
| limit          | query| integer | No      | Number of interfaces to return in a page |
+----------------+------+---------+---------+------------------------------------------+
| marker         | query| integer | No      | Last interface ID of the previous page   |
+----------------+------+---------+---------+------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Interface List
******************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-interfaces" \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-------------------+------+---------+-------------------------------------------------+
| Name              | In   | Type    | Description                                     |
+===================+======+=========+=================================================+
| network-interface | body | array   | Array of network interface objects              |
+-------------------+------+---------+-------------------------------------------------+
| created_at        | body | string  | Timestamp of network interface creation         |
+-------------------+------+---------+-------------------------------------------------+
| updated_at        | body | string  | Timestamp of last network interface update      |
+-------------------+------+---------+-------------------------------------------------+
| name              | body | string  | Name of the interface                           |
+-------------------+------+---------+-------------------------------------------------+
| id                | body | integer | Unique ID of the network interface              |
+-------------------+------+---------+-------------------------------------------------+
| device_id         | body | integer | Unique ID of the interface's device             |
+-------------------+------+---------+-------------------------------------------------+
| network_id        | body | integer | Unique ID of the interfaces's netowrk           |
+-------------------+------+---------+-------------------------------------------------+
| interface_type    | body | string  | Type of network interface                       |
+-------------------+------+---------+-------------------------------------------------+
| project_id        | body | string  | ID of the network interface's project           |
+-------------------+------+---------+-------------------------------------------------+
| vlan_id           | body | integer | ID of the VLAN of the network interface         |
+-------------------+------+---------+-------------------------------------------------+
| vlan              | body | string  | virtual local area netowrk of the interface     |
+-------------------+------+---------+-------------------------------------------------+
| port              | body | integer | Number of the port of the network interface     |
+-------------------+------+---------+-------------------------------------------------+
| duplex            | body | string  | Operation type of network interface             |
+-------------------+------+---------+-------------------------------------------------+
| speed             | body | integer | Bandwidth of the netork interface               |
+-------------------+------+---------+-------------------------------------------------+
| link              | body | string  | Channel between network interfaces              |
+-------------------+------+---------+-------------------------------------------------+
| cdp               | body | string  | Cisco Discovery Protocol                        |
+-------------------+------+---------+-------------------------------------------------+
| security          | body | string  | Security protocol of the network interface      |
+-------------------+------+---------+-------------------------------------------------+
| ip_address        | body | string  | Internet protocol address of the interface      |
+-------------------+------+---------+-------------------------------------------------+
| labels            | body | string  | User defined labels                             |
+-------------------+------+---------+-------------------------------------------------+
| note              | body | string  | Note used for governance                        |
+-------------------+------+---------+-------------------------------------------------+
| variables         | body | object  | User defined variables                          |
+-------------------+------+---------+-------------------------------------------------+

Example Network Interface List
******************************

.. code-block:: json

   [
      {
         "cdp": null,
         "device_id": 1,
         "duplex": null,
         "id": 1,
         "interface_type": "ethernet",
         "ip_address": "10.10.0.1",
         "link": null,
         "name": "myNetInterface",
         "network_id": null,
         "port": null,
         "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
         "security": null,
         "speed": null,
         "vlan": null,
         "vlan_id": null
      },
      {
         "cdp": null,
         "device_id": 1,
         "duplex": null,
         "id": 2,
         "interface_type": "ethernet",
         "ip_address": "10.10.0.2",
         "link": null,
         "name": "myNetInterface2",
         "network_id": null,
         "port": null,
         "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
         "security": null,
         "speed": null,
         "vlan": null,
         "vlan_id": null
      }
   ]

.. todo:: **Example Unexpected Error**

 ..literalinclude:: ./api_samples/errors/errors-unexpected-resp.json
    :language: javascript

Update Network Interface
========================

:PUT: /v1/network-interfaces/{id}

Update an existing network interface

Normal response codes: OK(200)

Error response codes: invalid request(400), interface not found(404), validation exception(405)

Request
-------

+-------------------+------+---------+-------------------------------------------------+
| Name              | In   | Type    | Description                                     |
+===================+======+=========+=================================================+
| name              | body | string  | Name of the interface                           |
+-------------------+------+---------+-------------------------------------------------+
| interface_type    | body | string  | Type of network interface                       |
+-------------------+------+---------+-------------------------------------------------+
| vlan              | body | string  | virtual local area netowrk of the interface     |
+-------------------+------+---------+-------------------------------------------------+
| port              | body | integer | Number of the port of the network interface     |
+-------------------+------+---------+-------------------------------------------------+
| duplex            | body | string  | Operation type of network interface             |
+-------------------+------+---------+-------------------------------------------------+
| speed             | body | integer | Bandwidth of the netork interface               |
+-------------------+------+---------+-------------------------------------------------+
| link              | body | string  | Channel between network interfaces              |
+-------------------+------+---------+-------------------------------------------------+
| cdp               | body | string  | Cisco Discovery Protocol                        |
+-------------------+------+---------+-------------------------------------------------+
| security          | body | string  | Security protocol of the network interface      |
+-------------------+------+---------+-------------------------------------------------+
| labels            | body | string  | User defined labels                             |
+-------------------+------+---------+-------------------------------------------------+
| note              | body | string  | Note used for governance                        |
+-------------------+------+---------+-------------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Interface Update
********************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-interfaces/1" \
      -XPUT \
      -d '{"name": "newNetInterface", "speed": 1000, "duplex": "full", "port": "80"}' \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+-------------------+------+---------+-------------------------------------------------+
| Name              | In   | Type    | Description                                     |
+===================+======+=========+=================================================+
| created_at        | body | string  | Timestamp of network interface creation         |
+-------------------+------+---------+-------------------------------------------------+
| updated_at        | body | string  | Timestamp of last network interface update      |
+-------------------+------+---------+-------------------------------------------------+
| name              | body | string  | Name of the interface                           |
+-------------------+------+---------+-------------------------------------------------+
| id                | body | integer | Unique ID of the network interface              |
+-------------------+------+---------+-------------------------------------------------+
| device_id         | body | integer | Unique ID of the interface's device             |
+-------------------+------+---------+-------------------------------------------------+
| network_id        | body | integer | Unique ID of the interfaces's netowrk           |
+-------------------+------+---------+-------------------------------------------------+
| interface_type    | body | string  | Type of network interface                       |
+-------------------+------+---------+-------------------------------------------------+
| project_id        | body | string  | ID of the network interface's project           |
+-------------------+------+---------+-------------------------------------------------+
| vlan_id           | body | integer | ID of the VLAN of the network interface         |
+-------------------+------+---------+-------------------------------------------------+
| vlan              | body | string  | virtual local area netowrk of the interface     |
+-------------------+------+---------+-------------------------------------------------+
| port              | body | integer | Number of the port of the network interface     |
+-------------------+------+---------+-------------------------------------------------+
| duplex            | body | string  | Operation type of network interface             |
+-------------------+------+---------+-------------------------------------------------+
| speed             | body | integer | Bandwidth of the netork interface               |
+-------------------+------+---------+-------------------------------------------------+
| link              | body | string  | Channel between network interfaces              |
+-------------------+------+---------+-------------------------------------------------+
| cdp               | body | string  | Cisco Discovery Protocol                        |
+-------------------+------+---------+-------------------------------------------------+
| security          | body | string  | Security protocol of the network interface      |
+-------------------+------+---------+-------------------------------------------------+
| ip_address        | body | string  | Internet protocol address of the interface      |
+-------------------+------+---------+-------------------------------------------------+
| labels            | body | string  | User defined labels                             |
+-------------------+------+---------+-------------------------------------------------+
| note              | body | string  | Note used for governance                        |
+-------------------+------+---------+-------------------------------------------------+
| variables         | body | object  | User defined variables                          |
+-------------------+------+---------+-------------------------------------------------+

Example Network Interface Update
********************************

.. code-block:: json

   {
      "cdp": null,
      "device_id": 1,
      "duplex": "full",
      "id": 1,
      "interface_type": "ethernet",
      "ip_address": "10.10.0.1",
      "link": null,
      "name": "newNetInterface",
      "network_id": null,
      "port": "80",
      "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06",
      "security": null,
      "speed": 1000,
      "vlan": null,
      "vlan_id": null
   }

Update Network Interface Variables
==================================

:PUT: /v1/network-interfaces/{id}/variables

Update user defined variables for the network interface

Normal response codes: OK(200)

Error response codes: invalid request(400), interface not found(404), validation exception(405)

Request
-------

+--------+------+---------+--------------------------------------------------+
| Name   | In   | Type    | Description                                      |
+========+======+=========+==================================================+
| key    | body | string  | Identifier                                       |
+--------+------+---------+--------------------------------------------------+
| value  | body | object  | Data                                             |
+--------+------+---------+--------------------------------------------------+
| id     | path | integer | Unique ID of the network interface to be updated |
+--------+------+---------+--------------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Interface Variables Update
******************************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/network-interfaces/1/variables" \
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

Example Network Interface Variables Update
******************************************

.. code-block:: json

   {
      "variables":
       {
          "newVar": "sample variable"
       }
   }

Delete Network Interface
========================

:DELETE: /v1/network-interfaces/{id}

Deletes an existing record of a network interface

Normal response codes: no content(204)

Error response codes: invalid request(400), interface not found(404)

Request
-------

+--------+------+---------+-------------------------------------------------+
| Name   | In   | Type    | Description                                     |
+========+======+=========+=================================================+
| id     | path | integer | Unique ID of the network interface to be deleted|
+--------+------+---------+-------------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE

Delete Network Interface Variables
==================================

:DELETE: /v1/network-interfaces/{id}/variables

Delete existing key/value variables for the network interface

Normal response codes: no content(204)

Error response codes: invalid request(400), interface not found(404) validation exception(405)

Request
-------

+--------+------+---------+-----------------------------------+
| Name   | In   | Type    | Description                       |
+========+======+=========+===================================+
| id     | path | integer | Unique ID of the network interface|
+--------+------+---------+-----------------------------------+
| key    | body | string  | Identifier to be deleted          |
+--------+------+---------+-----------------------------------+
| value  | body | object  | Data to be deleted                |
+--------+------+---------+-----------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Response
--------

No body content is returned on a successful DELETE
