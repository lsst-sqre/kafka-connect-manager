#####################
kafka-connect-manager
#####################

Python client for managing Kafka connectors.

Features
========

* List, create, and delete connectors
* Get info, status, pause, resume and restart an existing connector
* k8s deployment via `Helm chart <https://lsst-sqre.github.io/charts/>`_.

Supported connectors
====================

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


  See `the docs <https://kafka-connect-manager.lsst.io>`_ for more information.
