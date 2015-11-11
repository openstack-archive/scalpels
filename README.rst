Scalpels
========
Scalpels is distributed tracing or digging system for OpenStack.

Background
==========
OpenStack is made of multiple Python-based projects. Each project has similiar but different architecture. Scalpels gathers useful scripts or 3rd tools to help operator find what happen in your cloud.

Contribute
==========
This project is prototype now and under development. If you have interests in this work, please contact @kun_huang, at #openstack-chinese channel.

Single Node Architecture
========================
This type of deployment is used as POC in OpenStack community CI.

.. image:: doc/source/images/allinone.png
   :alt: All-in-One deployment

Multiple Node Architecture
==========================
This is under Designing:

.. image:: doc/source/images/multiple.png
   :alt: Multiple deployment

Ideas
=====
Each project will have scripts working:

* on python calls
* on sql queries
* on filesystem I/O
* on RPC calls if need
* on necessary system calls
* on common system statistics
