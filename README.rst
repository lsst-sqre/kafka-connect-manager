========================
kafka-connect-manager
========================

.. image:: https://img.shields.io/pypi/v/kafka-connect-manager.svg
   :target: https://pypi.python.org/pypi/kafka-connect-manager

.. image:: https://img.shields.io/pypi/pyversions/kafka-connect-manager.svg?style=flat-square
   :target: https://pypi.python.org/pypi/kafka-connect-manager

.. image:: https://travis-ci.com/lsst-sqre/kafka-connect-manager.svg
   :target: https://travis-ci.com/lsst-sqre/kafka-connect-manager

Python client for managing Confluent Kafka connectors

* Free software: GNU General Public License v3
* Documentation: https://kafka-connect-manager.lsst.io.


Features
--------

* List, create, and delete connectors
* Get info, status, pause, resume and restart an existing connector
* k8s deployment via `kafka-connect-manager <https://lsst-sqre.github.io/charts/>`_ Helm chart

Supported connectors
^^^^^^^^^^^^^^^^^^^^

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
