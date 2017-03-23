..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
 Craton URL Structure and Design
=================================

:Blueprint: https://blueprints.launchpad.net/craton/+spec/url-structure-and-design

Craton developers decided to start modifying the URL structure and semantics
prior to creating a release. This has led down a number of paths which require
documentation and understanding prior to resolving ourselves on one such
structure and semantic meaning.


Problem description
===================

Presently, Craton's API requires query parameters for certain calls. For
example,

- To list hosts, one **must** specify a region ID:

  .. code::

      GET /v1/hosts?region_id=1

- To list cells, one **must** specify a region ID:

  .. code::

      GET /v1/cells?region_id=1

To make the API easier to use for others, as well as easier to use when
performing checks across the inventory, Craton is looking to remove required
query parameters.


Proposed change
===============

Query parameters are typically optional and have always been a poorly considered
choice for a required parameter. Instead, the Craton team proposes that we
adopt a flat URL structure and design while continuing to allow filtering
based on attributes that were formerly required.

Now users will be able to list all hosts and cells that their project allows
them to view:

.. code::

    GET /v1/hosts
    GET /v1/cells

While also allowing them to filter those based on variables and other
attributes:

.. code::

    GET /v1/hosts?vars=operating_system:ubuntu
    GET /v1/cells?region_id=1

This change, however, will increase the priority of completing work around
adding pagination support to Craton. As such, adding support for pagination is
a work item of this specification.

Alternatives
------------

We could retain our current way of using query parameters. This, however, is
unseemly, unusual, and an unpleasant experience for users. If we were to
continue requiring parameters, e.g., ``region_id``, we would instead be
adopting a dfifferent URL structure.

Data model impact
-----------------

There are no database or data model impacts implied by this change.

REST API impact
---------------

This makes the API easier to use and reason about for users new to Craton's
API.

Security impact
---------------

Proper pagination support is necessary to prevent requests returning large
collections of resources.

Notifications impact
--------------------

Craton does not presently have notifications, so there is no impact.

Other end user impact
---------------------

This will affect the command-line interface to cratonclient. As region IDs are
no longer necessary for listing resources, that requirement will need to be
relaxed in our parameter handling.

Performance Impact
------------------

With proper pagination, this should have a neglible (if any) impact on
Craton's performance.

Other deployer impact
---------------------

This will not affect people who are deploying Craton.

Developer impact
----------------

This has no other developer impact beyond API usage.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
- git-harry

Other contributors:
- icordasc

Work Items
----------

- Refactor API layer to stop requiring parameters in the query string (See
  also: https://review.openstack.org/408016)

- Add pagination support for endpoints returning collections of resources.


Dependencies
============

N/A


Testing
=======

We will update and continue to use our current functional testing.


Documentation Impact
====================

This will affect the API reference section of our documentation.


References
==========

* https://review.openstack.org/408016

* https://review.openstack.org/400198

* https://review.openstack.org/401958
