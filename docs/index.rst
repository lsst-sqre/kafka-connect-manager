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

  * `Lenses InfluxDB Sink <https://docs.lenses.io/connectors/sink/influx.html>`_

    * Scripted configuration

    * Dynamically check existing topics in Kafka and update the connector configuration

    * Skip topic names added to a blacklist

    * Select timestamp field to use as the InfluxDB time

    * Error handling


  * `Confluent Replicator <https://docs.confluent.io/5.3.1/connect/kafka-connect-replicator/index.html>`_

    * Scripted configuration

    * Dynamically poll the source cluster for new topics

    * Support topic replication and schema continuous migration

    * Skip topic names added to a blacklist

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
