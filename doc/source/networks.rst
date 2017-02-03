.. _networks:

========
Networks
========

Definition of network

Create Network
==============

:POST: /v1/networks

Create a new network

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+---------------+------+---------+------------------------------------+
| Name          | In   | Type    | Description                        |
+===============+======+=========+====================================+
| created_at    | body | string  | Timestamp of network creation      |
+---------------+------+---------+------------------------------------+
| updated_at    | body | string  | Timestamp of last network update   |
+---------------+------+---------+------------------------------------+
| name          | body | string  | Name of the network                |
+---------------+------+---------+------------------------------------+
| id            | body | integer | Unique ID of the network           |
+---------------+------+---------+------------------------------------+
| cell_id       | body | integer | Unique ID of the network's cell    |
+---------------+------+---------+------------------------------------+
| region_id     | body | integer | Unique ID of the network's region  |
+---------------+------+---------+------------------------------------+
| project_id    | body | integer | ID of the network's project        |
+---------------+------+---------+------------------------------------+
| cidr          | body | string  | Network prefix                     |
+---------------+------+---------+------------------------------------+
| gateway       | body | string  | Default gateway IP of the network  |
+---------------+------+---------+------------------------------------+
| netmask       | body | string  | Network subnet mask                |
+---------------+------+---------+------------------------------------+
| ip_block_type | body | string  | Network type                       |
+---------------+------+---------+------------------------------------+
| nss           | body | string  | Network segmentation size          |
+---------------+------+---------+------------------------------------+
| labels        | body | string  | User defined labels                |
+---------------+------+---------+------------------------------------+
| note          | body | string  | Note used for governance           |
+---------------+------+---------+------------------------------------+
| variables     | body | string  | User defined variables             |
+---------------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Create
**********************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/networks" \
       -d '{"name": "myNetwork", "cidr": "192.168.1.1", "gateway": "192.168.1.0", "netmask": "255.255.255.0", "region_id": 1}' \
       -H "Content-Type: application/json" \
       -H "X-Auth-Token: demo" \
       -H "X-Auth-User: demo" \
       -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+---------------+------+---------+------------------------------------+
| Name          | In   | Type    | Description                        |
+===============+======+=========+====================================+
| network       | body | object  | - created_at                       |
|               |      |         | - updated_at                       |
|               |      |         | - name                             |
|               |      |         | - id                               |
|               |      |         | - cell_id                          |
|               |      |         | - region_id                        |
|               |      |         | - project_id                       |
|               |      |         | - cidr                             |
|               |      |         | - gateway                          |
|               |      |         | - nss                              |
|               |      |         | - labels                           |
|               |      |         | - note                             |
|               |      |         | - variables                        |
+---------------+------+---------+------------------------------------+
| created_at    | body | string  | Timestamp of network creation      |
+---------------+------+---------+------------------------------------+
| updated_at    | body | string  | Timestamp of last network update   |
+---------------+------+---------+------------------------------------+
| name          | body | string  | Name of the network                |
+---------------+------+---------+------------------------------------+
| id            | body | integer | Unique ID of the network           |
+---------------+------+---------+------------------------------------+
| cell_id       | body | integer | Unique ID of the network's cell    |
+---------------+------+---------+------------------------------------+
| region_id     | body | integer | Unique ID of the network's region  |
+---------------+------+---------+------------------------------------+
| project_id    | body | integer | ID of the network's project        |
+---------------+------+---------+------------------------------------+
| cidr          | body | string  | Network prefix                     |
+---------------+------+---------+------------------------------------+
| gateway       | body | string  | Default gateway IP of the network  |
+---------------+------+---------+------------------------------------+
| netmask       | body | string  | Network subnet mask                |
+---------------+------+---------+------------------------------------+
| ip_block_type | body | string  | Network type                       |
+---------------+------+---------+------------------------------------+
| nss           | body | string  | Network segmentation size          |
+---------------+------+---------+------------------------------------+
| labels        | body | string  | User defined labels                |
+---------------+------+---------+------------------------------------+
| note          | body | string  | Note used for governance           |
+---------------+------+---------+------------------------------------+
| variables     | body | string  | User defined variables             |
+---------------+------+---------+------------------------------------+

Example Network Create
**********************

.. code-block:: json

   {
      "cell_id": 1,
      "cidr": "192.168.0.0",
      "gateway": "192.168.1.0",
      "id": 1, "ip_block_type": null,
      "name": "myNet",
      "netmask": "255.255.255.0",
      "nss": null,
      "region_id": 1
   }

List Network
============

:GET: /v1/networks

Gets all existing networks

Normal response codes: OK(200)

Error response codes: invalid request(400), network not found(404), validation exception(405)

Request
-------

+--------------+------+---------+---------+---------------------------------------+
| Name         | In   | Type    | Required| Description                           |
+==============+======+=========+=========+=======================================+
| id           | query| integer | No      | ID of the network to get              |
+--------------+------+---------+---------+---------------------------------------+
| network_type | query| string  | No      | Type of the network to get            |
+--------------+------+---------+---------+---------------------------------------+
| name         | query| string  | No      | Name of the network to get            |
+--------------+------+---------+---------+---------------------------------------+
| region_id    | query| string  | No      | Region id of the network to get       |
+--------------+------+---------+---------+---------------------------------------+
| vars         | query| string  | No      | Variable filters to get networks      |
+--------------+------+---------+---------+---------------------------------------+
| cell_id      | query| string  | No      | Cell of the network to get            |
+--------------+------+---------+---------+---------------------------------------+
| limit        | query| integer | No      | Number of networks to return in a page|
+--------------+------+---------+---------+---------------------------------------+
| marker       | query| integer | No      | Last network ID of the previous page  |
+--------------+------+---------+---------+---------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network List
********************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/networks" \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+---------------+------+---------+------------------------------------+
| Name          | In   | Type    | Description                        |
+===============+======+=========+====================================+
| network       | body | array   | Array of network objects           |
+---------------+------+---------+------------------------------------+
| created_at    | body | string  | Timestamp of network creation      |
+---------------+------+---------+------------------------------------+
| updated_at    | body | string  | Timestamp of last network update   |
+---------------+------+---------+------------------------------------+
| name          | body | string  | Name of the network                |
+---------------+------+---------+------------------------------------+
| id            | body | integer | Unique ID of the network           |
+---------------+------+---------+------------------------------------+
| cell_id       | body | integer | Unique ID of the network's cell    |
+---------------+------+---------+------------------------------------+
| region_id     | body | integer | Unique ID of the network's region  |
+---------------+------+---------+------------------------------------+
| project_id    | body | integer | ID of the network's project        |
+---------------+------+---------+------------------------------------+
| cidr          | body | string  | Network prefix                     |
+---------------+------+---------+------------------------------------+
| gateway       | body | string  | Default gateway IP of the network  |
+---------------+------+---------+------------------------------------+
| netmask       | body | string  | Network subnet mask                |
+---------------+------+---------+------------------------------------+
| ip_block_type | body | string  | Network type                       |
+---------------+------+---------+------------------------------------+
| nss           | body | string  | Network segmentation size          |
+---------------+------+---------+------------------------------------+
| labels        | body | string  | User defined labels                |
+---------------+------+---------+------------------------------------+
| note          | body | string  | Note used for governance           |
+---------------+------+---------+------------------------------------+
| variables     | body | string  | User defined variables             |
+---------------+------+---------+------------------------------------+

Exapmle Network List
********************

.. code-block:: json

   [
      {
         "cell_id": 1,
         "cidr": "192.168.0.0",
         "gateway": "192.168.1.0",
         "id": 1,
         "ip_block_type": null,
         "name": "myNet",
         "netmask": "255.255.255.0",
         "nss": null,
         "region_id": 1
      },
      {
         "cell_id": null,
         "cidr": "192.168.0.15",
         "gateway": "192.168.1.0",
         "id": 3,
         "ip_block_type": null,
         "name": "myNetwork2",
         "netmask": "255.255.255.0",
         "nss": null,
         "region_id": 1
      }
   ]

.. todo:: **Example Unexpected Error**

Update Network
==============

:PUT: /v1/networks/{id}

Update an existing network

Normal response codes: OK(200)

Error response codes: invalid request(400), network not found(404), validation exception(405)

Request
-------

+------------+------+---------+------------------------------------+
| Name       | In   | Type    | Description                        |
+============+======+=========+====================================+
| name       | body | string  | Name of the network                |
+------------+------+---------+------------------------------------+
| cidr       | body | string  | Network prefix                     |
+------------+------+---------+------------------------------------+
| gateway    | body | string  | Default gateway IP of the network  |
+------------+------+---------+------------------------------------+
| netmask    | body | string  | Network subnet mask                |
+------------+------+---------+------------------------------------+
| nss        | body | string  | Network segmentation size          |
+------------+------+---------+------------------------------------+
| labels     | body | string  | User defined labels                |
+------------+------+---------+------------------------------------+
| note       | body | string  | Note used for governance           |
+------------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Update
**********************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/networks/1" \
      -XPUT \
      -d '{"name": "newName", "netmask": "0.0.0.0"}' \
      -H "Content-Type: application/json" \
      -H "X-Auth-Token: demo" \
      -H "X-Auth-User: demo" \
      -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+---------------+------+---------+------------------------------------+
| Name          | In   | Type    | Description                        |
+===============+======+=========+====================================+
| created_at    | body | string  | Timestamp of network creation      |
+---------------+------+---------+------------------------------------+
| updated_at    | body | string  | Timestamp of last network update   |
+---------------+------+---------+------------------------------------+
| name          | body | string  | Name of the network                |
+---------------+------+---------+------------------------------------+
| id            | body | integer | Unique ID of the network           |
+---------------+------+---------+------------------------------------+
| cell_id       | body | integer | Unique ID of the network's cell    |
+---------------+------+---------+------------------------------------+
| region_id     | body | integer | Unique ID of the network's region  |
+---------------+------+---------+------------------------------------+
| project_id    | body | integer | ID of the network device's project |
+---------------+------+---------+------------------------------------+
| cidr          | body | string  | Network prefix                     |
+---------------+------+---------+------------------------------------+
| gateway       | body | string  | Default gateway IP of the network  |
+---------------+------+---------+------------------------------------+
| netmask       | body | string  | Network subnet mask                |
+---------------+------+---------+------------------------------------+
| ip_block_type | body | string  | Network type                       |
+---------------+------+---------+------------------------------------+
| nss           | body | string  | Network segmentation size          |
+---------------+------+---------+------------------------------------+
| labels        | body | string  | User defined labels                |
+---------------+------+---------+------------------------------------+
| note          | body | string  | Note used for governance           |
+---------------+------+---------+------------------------------------+
| variables     | body | string  | User defined variables             |
+---------------+------+---------+------------------------------------+

Example Network Update
**********************

.. code-block:: json

   {
         "cell_id": 1,
         "cidr": "192.168.0.0",
         "gateway": "192.168.1.0",
         "id": 1,
         "ip_block_type": null,
         "name": "newName",
         "netmask": "0.0.0.0",
         "nss": null,
         "region_id": 1
   },

Update Network Variables
========================

:PUT: /v1/networks/{id}/variables

Update user defined variables for the network

Normal response codes: OK(200)

Error response codes: invalid request(400), network not found(404), validation exception(405)

Request
-------

+--------+------+---------+----------------------------------------------+
| Name   | In   | Type    | Description                                  |
+========+======+=========+==============================================+
| key    | body | string  | Identifier                                   |
+--------+------+---------+----------------------------------------------+
| value  | body | object  | Data                                         |
+--------+------+---------+----------------------------------------------+
| id     | path | integer | Unique ID of the network to be updated       |
+--------+------+---------+----------------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Network Variables Update
********************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/networks/1/variables" \
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

Example Network Variables Update
********************************

.. code-block:: json

   {
      "variables":
       {
          "newVar": "sample variable"
       }
   }

Delete Network
==============

:DELETE: /v1/networks/{id}

Deletes an existing record of a network

Normal response codes: no content(204)

Error response codes: invalid request(400), network not found(404)

Request
-------

+--------+------+---------+---------------------------------------+
| Name   | In   | Type    | Description                           |
+========+======+=========+=======================================+
| id     | path | integer | Unique ID of the network to be deleted|
+--------+------+---------+---------------------------------------+

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

:DELETE: /v1/networks/{id}/variables

Delete existing key/value variables for the network

Normal response codes: no content(204)

Error response codes: invalid request(400), network not found(404) validation exception(405)

Request
-------

+--------+------+---------+--------------------------------+
| Name   | In   | Type    | Description                    |
+========+======+=========+================================+
| id     | path | integer | Unique ID of the network       |
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
