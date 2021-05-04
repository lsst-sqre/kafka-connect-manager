
kafkaconnect helps to create and configure connectors in the Kafka Connect framework.
For non `dynamic connectors`_, kafkaconnect can be used as wrapper to auto-update
the connector configuration, for example, if topics are created or deleted in Kafka.

Kafkaconnect provides a command line interface (CLI) to interact with the `Kafka Connect API`_.
Using the CLI you can create managed connectors, or upload an a new one.
Kafkaconnect CLI can be used to validate a connector configuration, access the connector configuration properties, and return the validation output in case of errors.

Also, the `kafka-connect-manager helm chart`_ helps to deploy a connector on Kubernetes.

.. _dynamic connectors: https://www.confluent.io/blog/create-dynamic-kafka-connect-source-connectors/
.. _Kafka Connect API: https://docs.confluent.io/current/connect/references/restapi.html
.. _kafka-connect-manager helm chart: https://github.com/lsst-sqre/charts/tree/master/charts/kafka-connect-manager

Managed connectors
------------------

List of connectors we currently manage with kafkaconnect:

* `Lenses InfluxDB Sink`_
* `Confluent Amazon S3 Sink`_
* `Confluent JDBC Sink`_
* `MirrorMaker 2`_

.. _Lenses InfluxDB Sink: https://docs.lenses.io/connectors/sink/influx.html
.. _Confluent Amazon S3 Sink: https://docs.confluent.io/current/connect/kafka-connect-s3
.. _Confluent JDBC Sink: https://docs.confluent.io/kafka-connect-jdbc/current/sink-connector/index.html
.. _MirrorMaker 2: https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0

In principle, any connector installed in the `kafka-connect docker image`_ can also be managed by kafkaconnect using the ``upload`` command.

.. _kafka-connect docker image: https://github.com/lsst-sqre/kafka-connect-manager/tree/master/cp-kafka-connect
