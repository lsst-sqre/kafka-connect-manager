================
cp-kafka-connect
================

We build a specific ``cp-kafka-connect`` docker image with the connectors
managed by ``kafka-connect-manager``.

.. code::

  make cp-kafka-connect


Check the ``Makefile`` for the versions of each connector.

InfluxDB Sink connector
-----------------------

Download or build the connector from `stream-reactor <https://github.com/lsst-sqre/stream-reactor>`_.

Replicator connector
--------------------

Download the replicator connector from `kafka-connect-replicator <https://www.confluent.io/hub/confluentinc/kafka-connect-replicator>`_.
