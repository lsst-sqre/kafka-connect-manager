========================
cp-kafka-connect-manager
========================


.. image:: https://img.shields.io/pypi/v/cp-kafka-connect-manager.svg
        :target: https://pypi.python.org/pypi/cp-kafka-connect-manager

.. image:: https://img.shields.io/travis/lsst-sqre/cp-kafka-connect-manager.svg
        :target: https://travis-ci.org/lsst-sqre/cp-kafka-connect-manager

Python client for managing Confluent Kafka connectors

* Free software: GNU General Public License v3
* Documentation: https://cp-kafka-connect-manager.lsst.io.


Features
--------

* Support the following connectors: InfluxDB Sink
* List, create, and delete connectors
* Get info, status, pause, resume and restart an existing connector
* Auto-update - dynamically check existing topics in Kafka and update the
  configuration for an existing connector
* k8s deployment via ``cp-kafka-connect-manager`` Helm chart
