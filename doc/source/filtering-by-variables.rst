.. _filtering-by-variables:

================================
Filtering Resources by Variables
================================

This describes how to use variable queries when listing resources. This feature
uses a subset of JSON Path supported by `MySQL 5.7`_. Most notably, we do not
support the :code:`doubleAsterisk` component.

Supported Syntax
================

A variable query in our API consists of two main parts:

1. The JSON path
2. The JSON value

These are separated by a colon (:code:`:`).


You may supply as many of these as you like with each discrete query separated
by a comma (:code:`,`). For example, the following would all be valid queries
against the Craton API:

.. code-block:: text

   GET /v1/hosts?vars=hardware_profiles.disks[*].manufacturer:"Seagate"

and

.. code-block:: text

   GET /v1/hosts?vars="os-information".release.version:"4.4.0",hardware.core_count:12


Path
^^^^

The JSON Path expression is a series of path legs separated by a period ('.').
Each path leg can consist of the following components:

- A key, which can be either:

  - An `ECMAScript identifier`_, such as :code:`hardware_profiles` or
    :code:`release`.

  - A JSON_ string, such as :code:`"hyphenated-key"` or
    :code:`"this-is-a-json-string"`

- A key and an array wildcard or specific index, like :code:`foo[*]`,
  :code:`foo.bar[*].key`, or :code:`foo[3]`

- A wildcard character (:code:`*`), to specify all keys at this hierachical
  level, e.g. : :code:`foo.*.baz`


Value
^^^^^

The value portion of the query can consist of the following JSON data types:

- A JSON_ string, e.g. :code:`"this-is-a-json-string"`

- A JSON_ boolean, i.e. :code:`true` or :code:`false`

- A JSON_ null, i.e. :code:`null`

- A JSON_ integer, e.g. :code:`42`

- A JSON_ float, e.g. :code:`3.14`

Putting it All Together
=======================


Example 1
^^^^^^^^^

With this syntax, you can express powerful variable filters that afford for
searching through nested metadata on a resource. Here's a quick example to
illustrate the usefulness of this feature. Let's take some arbitrary hardware
data that's been stored for each of our hosts:

.. code-block:: json

    {
        "hardware_profiles": {
            "disks": [
                {
                    "manufacturer": "Seagate",
                    "capacity_quantity": 2,
                    "capacity_unit": "TB"
                },
                {
                    "manufacturer": "Western Digital",
                    "capacity_quantity": 3,
                    "capacity_unit": "TB"
                }
            ]
        }
    }


Now, let's say we want to find all of the hosts with a Seagate disk, one could
accomplish this with the following query:

.. code:: text

   GET /v1/hosts?vars=hardware_profiles.disks[*].manufacturer:"Seagate"


Example 2
^^^^^^^^^

As another example, let's say we're a root user for Craton (meaning we have
access across projects) - what if we wanted to get all hosts that are in, say,
any Region that is in some specific data center and the way we're representing
that on the Region resource(s) is:

.. code-block:: json

    {
        "datacenter_info": {
            "id": 543,
            "name": "DFW_DC_0"
        }
    }

Because of how variables are inherited by child resources, we could query for
all of these hosts by simply querying like so:

.. code-block:: text

   GET /v1/hosts?vars=datacenter_info.id:543


Limitations and Schema Considerations
=====================================

Known Limitations
^^^^^^^^^^^^^^^^^

- Because MySQL 5.7 does not support slicing arrays (:code:`foo[4:10]`, for
  instance), we do not support them in Craton.

- Although MySQL 5.7 does support the double-asterisk (:code:`prefix**suffix`)
  in its syntax, we do not. This is due to how `jsonpath-rw`, the library we
  use for parsing the API response, doesn't include the double-asterisk in its
  JSON path flavor.

- The first key in the path must be known, because it does not participate in
  the JSON column search. It is a separate field altogether, really, but we
  allow one to append it to the beginning for convenience in the syntax.

- You cannot use a colon (:code:`:`) in your JSON path or JSON value, since
  that is reserved for parsing the query itself.

- You cannot use a comma (:code:`,`) in your JSON path or JSON value, since
  that is reserved for parsing the query itself.

- When no rows are in the Variables table, JSON Path validation does not occur
  at the DB.

Schema Considerations
^^^^^^^^^^^^^^^^^^^^^

We do not officially support wildcard values in the Value portion of the
variables query. Therefore, it's a good idea to parse and store your data in a
more consistent and normalized manner. For instance, take the output of a
:bash:`uname` command in Linux, we'll use
:code:`Linux development 4.4.0-66-generic #87-Ubuntu SMP Fri Mar 3 15:29:05 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux`
as an example. One could parse this (or, preferably, use the variety of
:bash:`uname` flags that are available) and get several values from it. You may
want to store them in a variable on hosts as something like:

.. code-block:: json

    {
        "hardware": {
            "architecture": "x86_64",
            ...
        },
        "os": {
            "details": "Linux development 4.4.0-66-generic #87-Ubuntu SMP Fri Mar 3 15:29:05 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux",
            "distribution": "Ubuntu",
            "kernel": {
                "type": "Linux",
                "version": "4.4.0-66-generic",
                ...
            }
        }
    }

This will afford for easier matching against this data when trying to search,
so you can search for portions of the output of such a command, rather than
having to know the exact output. Also, there's more flexibility for searching
for similar things.


.. _`MySQL 5.7`: https://dev.mysql.com/doc/refman/5.7/en/json-path-syntax.html
.. _`ECMAScript Identifier`: https://www.ecma-international.org/ecma-262/5.1/#sec-7.6
.. _JSON: http://www.json.org/
