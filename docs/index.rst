###############
Connect manager
###############

Python client for managing the `Confluent Kafka connect REST Interface <https://docs.confluent.io/current/connect/references/restapi.html>`_.


Features
========

* List, create, and delete connectors
* Get info, status, pause, resume and restart an existing connector
* k8s deployment via `kafka-connect-manager <https://lsst-sqre.github.io/charts/>`_ Helm chart

Supported connectors
--------------------

* Landoop InfluxDB Sink

  * Scripted configuration

  * Dynamically check existing topics in Kafka and update the connector configuration

  * When configuring the connector skip topic names added to a blacklist


Installation
============

Install `kafka-connect-manager`:

.. code-block:: sh

  pip install kafka-connect-manager

User guide
==========

.. toctree::

   cli-reference
   api


Project information
===================

The main Git repository for `connect-mananer` is https://github.com/lsst-sqre/connect-manager

.. toctree::
   :maxdepth: 1

   contributing
   history

See the LICENSE_ file for licensing information.

.. _LICENSE: https://github.com/lsst-sqre/kafka-connect-manager/blob/master/LICENSE
