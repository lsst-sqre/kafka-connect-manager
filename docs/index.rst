#####################
Kafka-connect-manager
#####################

A Python client to configure and create connectors using the `Kafka Connect API <https://docs.confluent.io/current/connect/references/restapi.html>`_.

This site provides documentation for the kafka-connect-manager configuration, installation, user guide, development guide, and CLI reference.

To run kafka-connect-manager locally, you can jump straight to the `Configuration`_ and `User guide`_ sessions.

Overview
========

Kafka-connect-manager helps to configure and create Kafka connectors.
It can select Kafka topics using a regular expression and exclude topics added to a exclusion list.
The auto-update option dynamically updates the connector configuration if topics are created or deleted in Kafka.

Kafka-connect-manager can validate the connector configuration and return the validation output in case of errors.

Kafka-connect-manager provides a command line interface (CLI) to interact with the `Kafka Connect API <https://docs.confluent.io/current/connect/references/restapi.html>`_.
Using the CLI you can manage existing connectors or create a new one.

To deploy a supported connector, you can use the `kafka-connect-manager Helm chart <https://lsst-sqre.github.io/charts/>`_.

Supported connectors
--------------------
* `Lenses InfluxDB Sink <https://docs.lenses.io/connectors/sink/influx.html>`_
* `Amazon S3 Sink <https://docs.confluent.io/current/connect/kafka-connect-s3>`_


Installation
============

.. toctree::
   :maxdepth: 2

   installation

Configuration
=============

.. toctree::
   :maxdepth: 2

   configuration

User guide
==========

.. toctree::
   :maxdepth: 2

   userguide

Development guide
=================

.. toctree::
   :maxdepth: 2

   development
   release

CLI
===

.. toctree::
   :maxdepth: 2

   cli


Project information
===================

The GitHub repository for `kafka-connect-manager` is https://github.com/lsst-sqre/kafka-connect-manager

.. toctree::
   :maxdepth: 2

   contributing
   changelog

See the LICENSE_ file for licensing information.

.. _LICENSE: https://github.com/lsst-sqre/kafka-connect-manager/blob/master/LICENSE
