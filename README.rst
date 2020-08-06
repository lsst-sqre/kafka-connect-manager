#####################
kafka-connect-manager
#####################

|Build| |Docker|

A Python client to configure and create connectors using the `Kafka Connect API <https://docs.confluent.io/current/connect/references/restapi.html>`_.

Overview
========

Kafka-connect-manager helps to configure and create Kafka connectors. It can select Kafka topics using a regular expression and exclude topics added to a exclusion list. The auto-update option dynamically updates the connector if topics are created or deleted in Kafka.

Kafka-connect-manager can validate the connector configuration and return the validation output in case of errors.

Kafka-connect-manager provides a command line interface (CLI) to interact with the `Kafka Connect API <https://docs.confluent.io/current/connect/references/restapi.html>`_. Using the CLI you can manage existing connectors or create a new one.

To deploy a supported connector, you can use the `kafka-connect-manager Helm chart <https://lsst-sqre.github.io/charts/>`_.

Supported connectors
--------------------

* `Lenses InfluxDB Sink <https://docs.lenses.io/connectors/sink/influx.html>`_
* `Amazon S3 Sink <https://docs.confluent.io/current/connect/kafka-connect-s3>`_

See `the docs <https://kafka-connect-manager.lsst.io>`_ for more information.


.. |Build| image:: https://github.com/lsst-sqre/kafka-connect-manager/workflows/CI/badge.svg
  :alt: GitHub Actions
  :scale: 100%
  :target: https://github.com/lsst-sqre/kafka-connect-manager/actions

.. |Docker| image:: https://img.shields.io/docker/v/lsstsqre/kafkaconnect?sort=date
  :alt: Docker Hub repository
  :scale: 100%
  :target: https://hub.docker.com/repository/docker/lsstsqre/kafkaconnect
