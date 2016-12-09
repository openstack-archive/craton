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

In an effort to refactor some of the inner semantics, Craton's API is now
going to allow listing resources without these query parameters, e.g.,

- One may now list all hosts, regardless of region

  .. code::

      GET /v1/hosts

- One may now list all cells, regardless of region

  .. code::

      GET /v1/cells

This means that for deployments of Craton for large Fleets, we are introducing
a Denial of Service (a.k.a, DoS) vector for a simple GET request. (Presently
Craton does not support pagination.)

Forcing a limitation on how someone may interact with a resource is a natural
consequence of relations between resources and developing the API with
resilience in mind.


Proposed change
===============

Query parameters are typically optional and have always been a poorly considered
choice for a required parameter. Instead, the author of this specifiation
proposes that we express required attributes via the path itself, e.g.,

- To list hosts, one **must** specify a region ID:

  .. code::

      GET /v1/regions/1/hosts


- To list cells, one **must** specify a region ID:

  .. code::

      GET /v1/regions/1/cells

These constraints do not hold when considering projects due to the expression
and validation of project identifiers via authentication.

These constraints, when placed on the user, retain benefits of having
previously required these attributes while expressing them in a way that is
more obvious and far more common, not just in OpenStack but across the wide
expanse of HTTP APIs (RESTful and not).

This design alone, however, will not alone be enough to protect Craton from
DoS attack vectors, but it is a portion of the way to that end goal.

Alternatives
------------

We could retain our current way of using query parameters. This will, however,
hinder some of the refactoring in progress around inner details of how
Craton's API works.

We could first work with pagination and rate-limiting to avoid the DoS vector
that is introduced by allowing listing of devices across all regions. This is
significantly more work and potentially outside the current scope of work.

Data model impact
-----------------

There are no database or data model impacts implied by this change.

REST API impact
---------------

Much as the current work, this will drastically alter the semantics, look, and
feel of Craton's API.

.. todo::

    Once decided, I will update this section with the final impact
    description.

Security impact
---------------

.. todo::

    Again, I will update this with the final impact description. Some security
    impacts have been described above.

Notifications impact
--------------------

Craton does not presently have notifications, so there is no impact.

Other end user impact
---------------------

This will impact, in part, cratonclient. Modeling of the proposed behaviour on
the CLI will likely have no impact, the majority of impact will happen in the
API layer.

Performance Impact
------------------

.. todo::

    Based on the final decision I will update this later.

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

.. todo::

    Update this with decided work items.


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
