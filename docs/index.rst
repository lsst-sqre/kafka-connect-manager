###############
Connect manager
###############

Python client for managing the `Confluent Kafka connect REST Interface <https://docs.confluent.io/current/connect/references/restapi.html>`_.

Features
========

* Support the following Kafka connectors:

  * `Landoop InfluxDB Sink <https://docs.lenses.io/connectors/sink/influx.html>`_

* List, create, update, and delete connectors.
* Get connector info and status.
* Pause, resume and restart an existing connector.
* Auto-update: dynamically check for new topics in Kafka and update the
  connector configuration.
* Kubernetes deployment via ``connect-manager`` Helm chart.

Installation
============

Install `connect-manager`:

.. code-block:: sh

  pip install connect-manager

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
