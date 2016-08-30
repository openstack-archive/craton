Craton Inventory API 0.0.1
==========================

.. toctree::
    :maxdepth: 3


Description
~~~~~~~~~~

API for RPC Inventory Service



Contact Information
~~~~~~~~~~~~~~~~~~


Craton Developers




https://launchpad.net/~craton




License
~~~~~~


`Apache License <https://github.com/rackerlabs/craton/blob/master/LICENSE>`_




Base URL
~~~~~~~

http://craton.inventory.com/v1


Security
~~~~~~~


.. _securities_ApiKey:

ApiKey (API Key)
----------------



**Name:** api_key

**Located in:** header


I

CELLS
~~~~



PUT ``/cells/{id}``
-------------------


Summary
+++++++

Update an existing Cell


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of the cell


Request
+++++++




f
Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | 
        cell_uuid | No | string |  |  | UUID of the cell.
        name | Yes | string |  |  | 
        region | Yes | string |  |  | 
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        id | No | integer |  |  | Unique ID of the cell





**data schema:**



Any object ({})






.. code-block:: javascript

    {
        "status": "somestring", 
        "name": "somestring", 
        "region": "somestring", 
        "cell_uuid": "somestring", 
        "data": {}, 
        "id": 1
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/cells/{id}``
----------------------


Summary
+++++++

Delete an existing record of Cell


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of the cell


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



POST ``/cells``
---------------


Summary
+++++++

Create a new Cell



Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | 
        cell_uuid | No | string |  |  | UUID of the cell.
        name | Yes | string |  |  | 
        region | Yes | string |  |  | 
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        id | No | integer |  |  | Unique ID of the cell





**data schema:**



Any object ({})






.. code-block:: javascript

    {
        "status": "somestring", 
        "name": "somestring", 
        "region": "somestring", 
        "cell_uuid": "somestring", 
        "data": {}, 
        "id": 1
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



GET ``/cells``
--------------


Summary
+++++++

Get all cells


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        name | query | No | string |  | {"default": "None"} | name of the cell to get
        region | query | No | string |  | {"default": "None"} | name of the region to get cells for


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

An array of cells


Type: array of :ref:`Cell <d_ab97839b39e8f6ee5a7d95779ec7635f>`



**Example:**

.. code-block:: javascript

    [
        {
            "status": "somestring", 
            "name": "somestring", 
            "region": "somestring", 
            "cell_uuid": "somestring", 
            "data": {}, 
            "id": 1
        }, 
        {
            "status": "somestring", 
            "name": "somestring", 
            "region": "somestring", 
            "cell_uuid": "somestring", 
            "data": {}, 
            "id": 1
        }
    ]



**400**
^^^^^^^

Invalid Request



**default**
^^^^^^^^^^^

Unexpected error


Type: :ref:`Error <d_28c922c37a538ba224987a2662d49b53>`



**Example:**

.. code-block:: javascript

    {
        "fields": "somestring", 
        "message": "somestring", 
        "code": 1
    }



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



PUT ``/cells/{id}/data``
------------------------


Summary
+++++++

Update user defined data for the cell


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of Cell to update


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





**value schema:**



Any object ({})






.. code-block:: javascript

    {
        "value": {}, 
        "key": "somestring"
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/cells/{id}/data``
---------------------------


Summary
+++++++

Delete existing key/value data for the cell


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of Cell to update


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""


  

DATA
~~~



PUT ``/hosts/{id}/data``
------------------------


Summary
+++++++

Update user defined data for the server


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or hostname of the server to update


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





**value schema:**



Any object ({})






.. code-block:: javascript

    {
        "value": {}, 
        "key": "somestring"
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Host not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/hosts/{id}/data``
---------------------------


Summary
+++++++

Delete existing key/value data for the host


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or hostname of the server to update


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Host/data not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



PUT ``/regions/{id}/data``
--------------------------


Summary
+++++++

Update user defined data for the region


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of the region to update data


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





**value schema:**



Any object ({})






.. code-block:: javascript

    {
        "value": {}, 
        "key": "somestring"
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid ID supplied



**404**
^^^^^^^

Region not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/regions/{id}/data``
-----------------------------


Summary
+++++++

Delete existing key/value data for the region


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of the region to update data


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Region not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



PUT ``/cells/{id}/data``
------------------------


Summary
+++++++

Update user defined data for the cell


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of Cell to update


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





**value schema:**



Any object ({})






.. code-block:: javascript

    {
        "value": {}, 
        "key": "somestring"
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/cells/{id}/data``
---------------------------


Summary
+++++++

Delete existing key/value data for the cell


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of Cell to update


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Cell not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""


  

DEFAULT
~~~~~~



POST ``/regions``
-----------------


Summary
+++++++

Create a new Region



Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | Region Status.
        name | Yes | string |  |  | Region Name.
        cells | No | array of :ref:`Cell <d_ab97839b39e8f6ee5a7d95779ec7635f>` |  |  | List of cells in this region
        project_id | No | string |  |  | ID of the project.
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        id | No | integer |  |  | Unique ID for the region.





**data schema:**



Any object ({})






.. code-block:: javascript

    {
        "status": "somestring", 
        "name": "somestring", 
        "cells": [
            {
                "status": "somestring", 
                "name": "somestring", 
                "region": "somestring", 
                "cell_uuid": "somestring", 
                "data": {}, 
                "id": 1
            }, 
            {
                "status": "somestring", 
                "name": "somestring", 
                "region": "somestring", 
                "cell_uuid": "somestring", 
                "data": {}, 
                "id": 1
            }
        ], 
        "project_id": "somestring", 
        "data": {}, 
        "id": 1
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**405**
^^^^^^^

Validation Exception


  


DELETE ``/regions/{id}``
------------------------


Summary
+++++++

Delete existing record of a region


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | 


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Region not found



**405**
^^^^^^^

Validation Exception


  

  

HOSTS
~~~~



PUT ``/hosts/{id}/data``
------------------------


Summary
+++++++

Update user defined data for the server


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or hostname of the server to update


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





**value schema:**



Any object ({})






.. code-block:: javascript

    {
        "value": {}, 
        "key": "somestring"
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Host not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/hosts/{id}/data``
---------------------------


Summary
+++++++

Delete existing key/value data for the host


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or hostname of the server to update


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Host/data not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



PUT ``/hosts/{id}``
-------------------


Summary
+++++++

Update an existing Host


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or hostname of the server


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | 
        service | Yes | array of string |  |  | 
        ip_address | Yes | string |  |  | 
        hostname | Yes | string |  |  | 
        id | No | integer |  |  | 
        cell | Yes | string |  |  | 
        hw_manufacturer | No | string |  |  | 
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        host_uuid | No | string |  |  | 





**data schema:**



Any object ({})






.. code-block:: javascript

    {
        "status": "somestring", 
        "service": [
            "somestring", 
            "somestring"
        ], 
        "data": {}, 
        "hostname": "somestring", 
        "host_uuid": "somestring", 
        "cell": "somestring", 
        "hw_manufacturer": "somestring", 
        "ip_address": "somestring", 
        "id": 1
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Host not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/hosts/{id}``
----------------------


Summary
+++++++

Delete existing record of host


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or hostname of the server


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Host not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



POST ``/hosts``
---------------


Summary
+++++++

Create a new Host



Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | 
        service | Yes | array of string |  |  | 
        ip_address | Yes | string |  |  | 
        hostname | Yes | string |  |  | 
        id | No | integer |  |  | 
        cell | Yes | string |  |  | 
        hw_manufacturer | No | string |  |  | 
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        host_uuid | No | string |  |  | 





**data schema:**



Any object ({})






.. code-block:: javascript

    {
        "status": "somestring", 
        "service": [
            "somestring", 
            "somestring"
        ], 
        "data": {}, 
        "hostname": "somestring", 
        "host_uuid": "somestring", 
        "cell": "somestring", 
        "hw_manufacturer": "somestring", 
        "ip_address": "somestring", 
        "id": 1
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



GET ``/hosts``
--------------


Summary
+++++++

Get all hosts


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        limit | query | No | integer |  | {"default": 1000, "exclusive_maximum": false, "minimum": 1, "exclusive_minimum": false, "maximum": 10000} | number of hosts to return
        name | query | No | string |  | {"default": "None"} | name of the hosts to get
        uuid | query | No | string |  | {"default": "None"} | UUID of host to get
        region | query | No | string |  | {"default": "None"} | name of the region to get hosts for
        cell | query | No | string |  | {"default": "None"} | name of the cell to get hosts for
        ip_address | query | No | string |  | {"default": "None"} | ip_address of the hosts to get
        service | query | No | array of string |  |  | Openstack service to query host by


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

An array of hosts


Type: array of :ref:`Host <d_c6cfeaf1a836dd8c99cf49bec2c87a33>`



**Example:**

.. code-block:: javascript

    [
        {
            "status": "somestring", 
            "service": [
                "somestring", 
                "somestring"
            ], 
            "data": {}, 
            "hostname": "somestring", 
            "host_uuid": "somestring", 
            "cell": "somestring", 
            "hw_manufacturer": "somestring", 
            "ip_address": "somestring", 
            "id": 1
        }, 
        {
            "status": "somestring", 
            "service": [
                "somestring", 
                "somestring"
            ], 
            "data": {}, 
            "hostname": "somestring", 
            "host_uuid": "somestring", 
            "cell": "somestring", 
            "hw_manufacturer": "somestring", 
            "ip_address": "somestring", 
            "id": 1
        }
    ]



**400**
^^^^^^^

Invalid Request



**default**
^^^^^^^^^^^

Unexpected error


Type: :ref:`Error <d_28c922c37a538ba224987a2662d49b53>`



**Example:**

.. code-block:: javascript

    {
        "fields": "somestring", 
        "message": "somestring", 
        "code": 1
    }



**404**
^^^^^^^

Host not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""


  

REGIONS
~~~~~~



GET ``/regions``
----------------


Summary
+++++++

Gets all Regions



Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

An array of regions


Type: array of :ref:`Region <d_9fbc6cec29a82ba7aa62f02b0d3f4426>`



**Example:**

.. code-block:: javascript

    [
        {
            "status": "somestring", 
            "name": "somestring", 
            "cells": [
                {
                    "status": "somestring", 
                    "name": "somestring", 
                    "region": "somestring", 
                    "cell_uuid": "somestring", 
                    "data": {}, 
                    "id": 1
                }, 
                {
                    "status": "somestring", 
                    "name": "somestring", 
                    "region": "somestring", 
                    "cell_uuid": "somestring", 
                    "data": {}, 
                    "id": 1
                }
            ], 
            "project_id": "somestring", 
            "data": {}, 
            "id": 1
        }, 
        {
            "status": "somestring", 
            "name": "somestring", 
            "cells": [
                {
                    "status": "somestring", 
                    "name": "somestring", 
                    "region": "somestring", 
                    "cell_uuid": "somestring", 
                    "data": {}, 
                    "id": 1
                }, 
                {
                    "status": "somestring", 
                    "name": "somestring", 
                    "region": "somestring", 
                    "cell_uuid": "somestring", 
                    "data": {}, 
                    "id": 1
                }
            ], 
            "project_id": "somestring", 
            "data": {}, 
            "id": 1
        }
    ]



**400**
^^^^^^^

Invalid Request



**default**
^^^^^^^^^^^

Unexpected Error


Type: :ref:`Error <d_28c922c37a538ba224987a2662d49b53>`



**Example:**

.. code-block:: javascript

    {
        "fields": "somestring", 
        "message": "somestring", 
        "code": 1
    }



**405**
^^^^^^^

Validation Exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



PUT ``/regions/{id}/data``
--------------------------


Summary
+++++++

Update user defined data for the region


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of the region to update data


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





**value schema:**



Any object ({})






.. code-block:: javascript

    {
        "value": {}, 
        "key": "somestring"
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid ID supplied



**404**
^^^^^^^

Region not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



DELETE ``/regions/{id}/data``
-----------------------------


Summary
+++++++

Delete existing key/value data for the region


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | UUID or name of the region to update data


Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Region not found



**405**
^^^^^^^

Validation exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""



PUT ``/regions/{id}``
---------------------


Summary
+++++++

Update an existing Region


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        id | path | Yes | string |  |  | 


Request
+++++++





Body
^^^^



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | Region Status.
        name | Yes | string |  |  | Region Name.
        cells | No | array of :ref:`Cell <d_ab97839b39e8f6ee5a7d95779ec7635f>` |  |  | List of cells in this region
        project_id | No | string |  |  | ID of the project.
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        id | No | integer |  |  | Unique ID for the region.





**data schema:**



Any object ({})






.. code-block:: javascript

    {
        "status": "somestring", 
        "name": "somestring", 
        "cells": [
            {
                "status": "somestring", 
                "name": "somestring", 
                "region": "somestring", 
                "cell_uuid": "somestring", 
                "data": {}, 
                "id": 1
            }, 
            {
                "status": "somestring", 
                "name": "somestring", 
                "region": "somestring", 
                "cell_uuid": "somestring", 
                "data": {}, 
                "id": 1
            }
        ], 
        "project_id": "somestring", 
        "data": {}, 
        "id": 1
    }


Responses
+++++++++


**200**
^^^^^^^

OK



**400**
^^^^^^^

Invalid Request



**404**
^^^^^^^

Region not found



**405**
^^^^^^^

Validation Exception


  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`ApiKey <securities_ApiKey>`, ""


  
  
Data Structures
~~~~~~~~~~~~~~




.. _d_ab97839b39e8f6ee5a7d95779ec7635f:


Cell Model Structure
--------------------



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | 
        cell_uuid | No | string |  |  | UUID of the cell.
        name | Yes | string |  |  | 
        region | Yes | string |  |  | 
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        id | No | integer |  |  | Unique ID of the cell





.. _i_029a7f936610667e90e2f1a720018ece:


**data schema:**



Any object ({})







.. _d_5badd2062470f8dd42cf8e0ee6745120:


Data Model Structure
--------------------



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        key | No | string |  |  | 
        value | No | :ref:`value <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  | 





.. _i_4d863967ef9a9d9efdadd1b250c76bd6:


**value schema:**



Any object ({})







.. _d_28c922c37a538ba224987a2662d49b53:


Error Model Structure
---------------------



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        fields | No | string |  |  | 
        message | No | string |  |  | 
        code | No | integer | int32 |  | 






.. _d_c6cfeaf1a836dd8c99cf49bec2c87a33:


Host Model Structure
--------------------



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | 
        service | Yes | array of string |  |  | 
        ip_address | Yes | string |  |  | 
        hostname | Yes | string |  |  | 
        id | No | integer |  |  | 
        cell | Yes | string |  |  | 
        hw_manufacturer | No | string |  |  | 
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        host_uuid | No | string |  |  | 





.. _i_029a7f936610667e90e2f1a720018ece:


**data schema:**



Any object ({})







.. _d_9fbc6cec29a82ba7aa62f02b0d3f4426:


Region Model Structure
----------------------



.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | string |  |  | Region Status.
        name | Yes | string |  |  | Region Name.
        cells | No | array of :ref:`Cell <d_ab97839b39e8f6ee5a7d95779ec7635f>` |  |  | List of cells in this region
        project_id | No | string |  |  | ID of the project.
        data | No | :ref:`data <i_029a7f936610667e90e2f1a720018ece>` |  |  | User defined information
        id | No | integer |  |  | Unique ID for the region.





.. _i_029a7f936610667e90e2f1a720018ece:


**data schema:**



Any object ({})






