

Kafkaconnect provides a command line interface (CLI) to interact with the `Kafka Connect API`_ and manage connectors.

For `dynamic connectors`_, the configuration is defined in a JSON file and uploaded to the Kafka Connect API.
For non dynamic connectors, kafkaconnect can be used as a wrapper to auto-update the connector configuration when topics are created or deleted in Kafka.

To deploy a connector on Kubernetes use the kafka-connect-manager `Helm chart`_.
For dynamic connectors, the configuration is stored in a configmap which is templated in Helm.

.. _dynamic connectors: https://www.confluent.io/blog/create-dynamic-kafka-connect-source-connectors/
.. _Kafka Connect API: https://docs.confluent.io/current/connect/references/restapi.html
.. _Helm chart: https://github.com/lsst-sqre/charts/tree/master/charts/kafka-connect-manager

Supported connectors
--------------------

List of connectors kafkaconnect currently supports:

* `Lenses InfluxDB Sink`_
* `Confluent Amazon S3 Sink`_ (dynamic)
* `Confluent JDBC Sink`_ (dynamic)
* `MirrorMaker 2`_ (dynamic)

.. _Lenses InfluxDB Sink: https://docs.lenses.io/connectors/sink/influx.html
.. _Confluent Amazon S3 Sink: https://docs.confluent.io/current/connect/kafka-connect-s3
.. _Confluent JDBC Sink: https://docs.confluent.io/kafka-connect-jdbc/current/sink-connector/index.html
.. _MirrorMaker 2: https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0

Note: other connectors can also be managed by kafkaconnect using the ``upload`` command, as long as they are installed in the `cp-kafka-connect docker image`_.

.. _cp-kafka-connect docker image: https://github.com/lsst-sqre/kafka-connect-manager/tree/master/cp-kafka-connect
