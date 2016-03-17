Minimum viable Craton
=====================

This is what we should build, as defined by `Eric Ries
<http://www.startuplessonslearned.com/2009/08/minimum-viable-product-guide.html>`_:

    [T]he minimum viable product is that version of a new product
    which allows a team to collect the maximum amount of validated
    learning about customers with the least effort.


Goals - end-to-end, with Ansible target; but deepen inventory


Process flow
============

MVP

- Manage inventory schema, along with corresponding YAML files from
  GitHub customer repos for config, PEM files/blobs
- Generate inventory file for Ansible, either for TaskFlow to drive
  overall; or for Ansible
- Run playbooks with respect to inventory
- Ansible callbacks for reachability, other errors
- TaskFlow notification to Redis
- Web view on progress, updated with changes ("cloud progress bar")


Logical architecture
====================

FIXME


Inventory database
==================

We will use a relational database to persist inventory
information. SQLAlchemy will be used for modeling, with Alembic
supporting migrations. For testing purposes, we expect SQLite to be
used; otherwise MySQL with Galera clustering is our target production
option. (This specifically may be Percona XtraDB.)

We will be using Ansible's inventory needs to drive these requirements:

- Hosts, identified by a synthetic `host_id`. Certain well-known host
  variables like IP address are available as nullable columns.
- Host variables/keys mapping, FK to hosts. This can also be used for
  extension attributes, eg to map to assets in a separate asset
  database.
- Groups, including subgroup relationships
- Secrets, FK to hosts, stores a PEM encoded blob (possibly other formats)
- References, FK to groups, to group variable YAML files (using URLs,
  eg to `GitHub refs <https://developer.github.com/v3/git/refs/>`_ or
  Swift storage; should we support blobs as well?)

In addition, we will support the following additional schema elements:

- Tenants - per customer, but a given customer may have multiple tenants.
- Regions - FK to tenant; hosts have a FK relationship to region.

In many cases, operators will deploy a single tenant/single region
inventory, but this gives flexibility in terms of where the inventory
database is located - possibly co-located with the cloud region or
driving it externally.

Workflows may be filtered by using standard SQLAlchemy queries with
respect to regions; specific hosts; host variables (tagging); and
groups

Queries against the inventory database produce materialized inventory
files (tarballs) typically stored in `/etc/ansible/`. These can be
produced in aggregate: run the inventory for a given playbook across
many hosts; or as a bundle of inventory files per host for running by
TaskFlow wrapping Ansible, with both zip file and tgz available,
similar to what GitHub supports for downloads. Note that all blobs are
included in these tarballs.

Lastly, the inventory database is completely encapsulated by a REST
API, making it pluggable. For example, it is possible that an existing
asset management system/CMDB could provide the desired functionality
provided here. Alternatively, a different backend can be written, eg
with MongoDB.


Asset management
----------------

We expect that most organizations will be using their own asset
management database in conjunction with this inventory database. Such
asset management would also be linked against long-term historical
data.


Secret management
-----------------

`Barbican <http://docs.openstack.org/developer/barbican/api/reference/secrets.html>`_


REST API
========

APIs are versioned, so we start all with `/v1`. ACLs are managed at
the REST API level, and are in done in conjunction with (optional)
Keystone middleware.

`GET /v1/tenants`
-----------------

Retrieves all registered tenants.

`GET /v1/regions/{tenant_id}`
-----------------------------

Retrieve a list of regions for a given tenant.


`GET /v1/inventory/{region_id}.tgz`
-----------------------------------

Retrieves the tgz tarball bundle for running with TaskFlow. Optional
parameters can specify for direct with Ansible; and query filters (eg
a specific host key/value or group/subgroup).

TODO: define corresponding `POST`, `PUT`, and `DELETE` verbs as it
makes sense. Plus this is obviously just the beginning of the REST
API; it is also currently just looking at inventory.


Python API
==========

Wraps the REST API above.


Scripting API
=============


Craton internals
================

Class layout FIXME (something initial with `tree` is probably good here)
