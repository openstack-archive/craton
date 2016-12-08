.. craton documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Craton's documentation!
==================================

Craton is a new project planned for OpenStack inclusion.
Craton supports deploying and operating OpenStack clouds by providing
scalable fleet management:

* Inventory of configurable physical devices/hosts (the fleet)
* Audit and remediation workflows against this inventory
* REST APIs, CLI, and Python client to manage

Support for workflows, CLI, and the Python client is in progress.



Getting Started
===============
.. toctree::
   :maxdepth: 1

   installation
   keystone
   cratoncli
   usage


Developer Guide
===============

.. toctree::
   :maxdepth: 1

   specs/index
   contributing
   architecture
   api-reference
   high-level-design


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


License
=======
Craton is licensed under the `Apache license <http://www.apache.org/licenses/LICENSE-2.0>`_
