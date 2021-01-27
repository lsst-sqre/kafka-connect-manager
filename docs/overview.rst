
kafkaconnect helps to configure and create Kafka connectors.
It can select Kafka topics using a regular expression and exclude topics added to a exclusion list.
The auto-update option dynamically updates the connector if topics are created or deleted in Kafka.

Kafkaconnect can validate the connector configuration and return the validation output in case of errors.

Kafkaconnect provides a command line interface (CLI) to interact with the `Kafka Connect API <https://docs.confluent.io/current/connect/references/restapi.html>`_.
Using the CLI you can manage existing connectors or create a new one.

To deploy a supported connector, you can use this `helm chart <https://github.com/lsst-sqre/charts/tree/master/charts/kafka-connect-manager>`_.

Supported connectors
--------------------

* `Lenses InfluxDB Sink <https://docs.lenses.io/connectors/sink/influx.html>`_
* `Amazon S3 Sink <https://docs.confluent.io/current/connect/kafka-connect-s3>`_
