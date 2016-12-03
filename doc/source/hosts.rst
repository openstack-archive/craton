.. _hosts:

=====
Hosts
=====

Definition of host

Create Host
===========

:POST: /v1/hosts

Create a new host

Normal response codes: OK(200)

Error response codes: invalid request(400), validation exception(405)

Request
-------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| variables  | body | object  | User defined variables        |
+------------+------+---------+-------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Host Create
*******************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/hosts" \
        -d '{"name": "fooHost", "region_id": 1, "ip_address": "11.11.11.14", "device_type": "Phone", "project_id": "717e9a216e2d44e0bc848398563bda06"}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| host       | body | object  | - id                          |
|            |      |         | - name                        |
|            |      |         | - cell_id                     |
|            |      |         | - region_id                   |
|            |      |         | - parent_id                   |
|            |      |         | - ip_address                  |
|            |      |         | - device_type                 |
|            |      |         | - active                      |
|            |      |         | - labels                      |
|            |      |         | - note                        |
|            |      |         | - variables                   |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the host         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| variables  | body | object  | User defined variables        |
+------------+------+---------+-------------------------------+

Examples Host Create
********************

.. code-block:: json

   {
      "active": true,
      "cell_id": null,
      "device_type": "Phone",
      "id": 1,
      "ip_address": "11.11.11.14",
      "name": "fooHost",
      "note": null,
      "parent_id": null,
      "region_id": 1
   }

List Hosts
==========

:GET: /v1/hosts?region_id=

Gets all Host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Default response: unexpected error

Request
-------

+------------+------+---------+---------+------------------------------+
| Name       | In   | Type    | Required| Description                  |
+============+======+=========+=========+==============================+
| region_id  | query| integer | Yes     | ID of the region to get hosts|
+------------+------+---------+---------+------------------------------+
| limit      | query| integer | No      | Number of host to return     |
|            |      |         |         | Ranging from 1 - 10000       |
+------------+------+---------+---------+------------------------------+
| name       | query| string  | No      | Name of the host to get      |
+------------+------+---------+---------+------------------------------+
| cell_id    | query| integer | No      | Name of the cell to get      |
+------------+------+---------+---------+------------------------------+
| ip         | query| string  | No      | IP address of the host to get|
+------------+------+---------+---------+------------------------------+
| device_type| query| string  | No      | Type of host to get          |
+------------+------+---------+---------+------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Examples Host List
******************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/hosts?region_id=1" \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| hosts      | body | array   | array of host                 |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the host         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| variables  | body | object  | User defined variables        |
+------------+------+---------+-------------------------------+

Examples Host List
******************

.. code-block:: json

   {
      "active": true,
      "cell_id": null,
      "device_type": "Computer", 
      "id": 2,
      "ip_address": "12.12.12.15",
      "name": "foo2Host",
      "note": null,
      "parent_id": null,
      "region_id": 1
   }, 
   {
      "active": true,
      "cell_id": null,
      "device_type": "Phone",
      "id": 1,
      "ip_address": "11.11.11.14",
      "name": "fooHost",
      "note": null,
      "parent_id": null,
      "region_id": 1
   }

.. todo:: **Example Unexpected Error**

 ..literalinclude:: ./api_samples/errors/errors-unexpected-resp.json
    :language: javascript

Update Hosts
============

:PUT: /v1/hosts/{id}

Update an existing host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

+------------+------+---------+------------------------------------+
| Name       | In   | Type    | Description                        |
+============+======+=========+====================================+
| name       | body | string  | Unique name of the host            |
+------------+------+---------+------------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell       |
+------------+------+---------+------------------------------------+
| region_id  | body | integer | Unique ID of the host's region     |
+------------+------+---------+------------------------------------+
| parent_id  | body | integer | ID of the host's parent            |
+------------+------+---------+------------------------------------+
| ip_address | body | string  | IP address of the host             |
+------------+------+---------+------------------------------------+
| device_type| body | string  | Type of host                       |
+------------+------+---------+------------------------------------+
| active     | body | boolean | State of host                      |
+------------+------+---------+------------------------------------+
| labels     | body | string  | User defined labels                |
+------------+------+---------+------------------------------------+
| note       | body | string  | Note used for governance           |
+------------+------+---------+------------------------------------+
| variables  | body | object  | User defined variables             |
+------------+------+---------+------------------------------------+
| id         | path | integer | Unique ID of the host to be updated|
+------------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Examples Host Update
********************

.. code-block:: bash 

   curl -i "http://${MY_IP}:8080/v1/hosts/2" \
        -XPUT \
        -d '{"name": "changedName"}' \
        -H "Content-Type: application/json" \
        -H "X-Auth-Token: demo" \
        -H "X-Auth-User: demo" \
        -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

Response
--------

+------------+------+---------+-------------------------------+
| Name       | In   | Type    | Description                   |
+============+======+=========+===============================+
| host       | body | object  | - id                          |
|            |      |         | - name                        |
|            |      |         | - cell_id                     |
|            |      |         | - region_id                   |
|            |      |         | - parent_id                   |
|            |      |         | - ip_address                  |
|            |      |         | - device_type                 |
|            |      |         | - active                      |
|            |      |         | - labels                      |
|            |      |         | - note                        |
|            |      |         | - variables                   |
+------------+------+---------+-------------------------------+
| id         | body | integer | Unique ID of the host         |
+------------+------+---------+-------------------------------+
| name       | body | string  | Unique name of the host       |
+------------+------+---------+-------------------------------+
| cell_id    | body | integer | Unique ID of the host's cell  |
+------------+------+---------+-------------------------------+
| region_id  | body | integer | Unique ID of the host's region|
+------------+------+---------+-------------------------------+
| parent_id  | body | integer | ID of the host's parent       |
+------------+------+---------+-------------------------------+
| ip_address | body | string  | IP address of the host        |
+------------+------+---------+-------------------------------+
| device_type| body | string  | Type of host                  |
+------------+------+---------+-------------------------------+
| active     | body | boolean | State of host                 |
+------------+------+---------+-------------------------------+
| labels     | body | string  | User defined labels           |
+------------+------+---------+-------------------------------+
| note       | body | string  | Note used for governance      |
+------------+------+---------+-------------------------------+
| variables  | body | object  | User defined variables        |
+------------+------+---------+-------------------------------+

Example Host Update
*******************

.. code-block:: json

   {
      "active": true,
      "cell_id": null,
      "device_type": "Computer",
      "id": 2, 
      "ip_address": "12.12.12.15",
      "name": "changedName", 
      "note": null, 
      "project_id": "717e9a21-6e2d-44e0-bc84-8398563bda06", 
      "region_id": 1
   }

Update Host variables
=====================

:PUT: /v1/hosts/{id}/variables

Update user defined variables for the host

Normal response codes: OK(200)

Error response codes: invalid request(400), host not found(404), validation exception(405)

Request
-------

+--------+------+---------+------------------------------------+
| Name   | In   | Type    | Description                        |
+========+======+=========+====================================+
| key    | body | string  | Identifier                         |
+--------+------+---------+------------------------------------+
| value  | body | object  | Data                               |
+--------+------+---------+------------------------------------+
| id     | path | integer | Unique ID of the host to be updated|
+--------+------+---------+------------------------------------+

Required Header
^^^^^^^^^^^^^^^

- Content-Type: application/json
- X-Auth-Token
- X-Auth-User
- X-Auth-Project

Example Host Variables Update
*****************************

.. code-block:: bash

   curl -i "http://${MY_IP}:8080/v1/hosts/1/variables" \
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

Example Host Variables Update
*****************************

.. code-block:: json

   {
      "variables": {
                      "newVar": "sample variable"
                   }
   }

Delete Host
===========

:DELETE: /v1/hosts/{id}

Deletes an existing record of a Host

Normal response codes: no content(204)

Error response codes: invalid request(400), host not found(404)

Request
-------

+--------+------+---------+------------------------------------+
| Name   | In   | Type    | Description                        |
+========+======+=========+====================================+
| id     | path | integer | Unique ID of the host to be deleted|
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

Delete Host Variables
=====================

:DELETE: /v1/hosts/{id}/variables

Delete existing key/value variables for the Host

Normal response codes: no content(204)

Error response codes: invalid request(400), host not found(404) validation exception(405)

Request
-------

+--------+------+---------+-------------------------+
| Name   | In   | Type    | Description             |
+========+======+=========+=========================+
| id     | path | integer | Unique ID of the host   |
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
