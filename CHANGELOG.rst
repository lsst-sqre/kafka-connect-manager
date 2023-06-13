##########
Change log
##########

1.2.0 (2023-06-12)
==================

* Add support to Strimzi Kafka 0.35.1 and Kafka 3.4.0

1.1.0 (2023-05-28)
==================

* Add support to tags in the InfluxDB Sink connector
* Add support to Strimzi Kafka 0.34.0 and Kafka 3.3.1

1.0.2 (2023-01-13)
==================

* Add support to Strimzi Kafka 0.32.0 and Kafka 3.3.1.

1.0.0 (2022-07-09)
==================

* Add support to Strimzi Kafka 0.29.0 and Kafka 3.1.1.
* Build Strimzi Kafka image with a special version of the InfluxDB Sink connector plugin which supports timestamps in microseconds.
* Build Strimzi Kafka image with Kafka Connect Avro Converter plugin.
* New class TopicNamesSet
* Add SASL authentication to Kafka brokers

0.9.3 (2021-10-29)
==================

* Refactor S3 Sink connector, it now expects a configuration file which is templated in the Helm chart.
* Updated docs.

0.9.1 (2021-06-09)
==================

* Add support to configure multiple InfluxDB Sink connectors.
* Add user guide documentation on how to reset the InfluxDB Sink connector consumer group offsets.
* Update ``cp-kafka-connect`` image with new version of the InfluxDB Sink Connector. See `#737 <https://github.com/lensesio/stream-reactor/issues/737>`_ for details.

0.9.0 (2021-05-03)
==================

* Add ``create mirrormaker2`` command
* Add ``create jdbc-sink`` command
* Update dependencies


0.8.3 (2021-03-04)
==================

* Add upload command
* Initial support to MirrorMaker 2 and Confuent JDBC Sink Connectors
* Update dependencies

0.8.2 (2021-01-25)
==================

* Update ``cp-kafka-connect`` image with new version of the InfluxDB Sink connector. This version bumps the ``influxdb-java`` dependency from version 2.9 to 2.21. In particular 2.16 introduced a fix to skip fields with ``NaN`` and ``Infinity`` values when writing to InfluxDB.
* Reorganize developer and user guides.
* Add documentation in the user guide on how to run the InfluxDB Sink connector locally.
* Update dependencies

0.8.1 (2020-10-18)
==================

* Fix bug preventing to read InfluxDB password from the environment
* Update ``cp-kafka-connect`` image with Confluent Platform 5.5.2
* Update dependencies

0.8.0 (2020-08-05)
==================

* Use data classes for the application and connector configuration.
* Plugin like organization, to support new connectors add a cli and a config file.
* Add support to the Amazon S3 Sink connector

0.7.2 (2020-03-31)
==================

* Add support to the InfluxDB Sink Connector.
* Add --timestamp option to select the timestamp field to use in the InfluxDB Sink connector.
* Fix Header Converter Class configuration setting.
* Fix ``tasks.max`` configuration setting name.
* Add connector ``name`` configuration setting to support multiple connectors of the same class.
* Handle empty list of topics properly.
