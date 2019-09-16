========================
kafka-connect-manager
========================


.. image:: https://img.shields.io/pypi/v/kafka-connect-manager.svg
        :target: https://pypi.python.org/pypi/kafka-connect-manager

.. image:: https://img.shields.io/travis/lsst-sqre/kafka-connect-manager.svg
        :target: https://travis-ci.org/lsst-sqre/kafka-connect-manager

Python client for managing Confluent Kafka connectors

* Free software: GNU General Public License v3
* Documentation: https://kafka-connect-manager.lsst.io.


Features
--------

* List, create, and delete connectors
* Get info, status, pause, resume and restart an existing connector
* k8s deployment via ``kafka-connect-manager`` Helm chart

Specific features for supported connectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Landoop InfluxDB Sink:
  - Scripted configuration
  - Dynamically check existing topics in Kafka and update the connector configuration (*--auto-update*)
  - When configuring the connector skip topic names added to a
    blacklist (*--blacklist*)
