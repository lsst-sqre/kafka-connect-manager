##################
Using kafkaconnect
##################

Lenses InfluxDB Sink
====================

In this section, we use kafkaconnect to create an instance of the `Lenses InfluxDB Sink <https://docs.lenses.io/connectors/sink/influx.html>`_ connector.
We show the connector in action by producing messages to a kafka topic and query the messages recorded in InfluxDB.

Download the docker-compose_ file and start the services:

.. _docker-compose: https://github.com/lsst-sqre/kafka-connect-manager/blob/master/tests/docker-compose.yml

.. code-block:: bash

  docker-compose up -d

Create the `foo` topic in kafka:

.. code-block:: bash

  docker-compose exec broker kafka-topics --bootstrap-server broker:9092 --create --topic foo --partitions 1 --replication-factor 1

Create the `mydb` database in InfluxDB:

.. code-block:: bash

  docker-compose exec influxdb influx -execute "CREATE DATABASE mydb"

Use kafka-connect-manager to create an instance of the InfluxDB Sink connector.

.. code-block:: bash

  docker-compose run kafkaconnect create influxdb-sink -d mydb foo

You can check if the connector is running by using the `status` command:

.. code-block:: bash

  docker-compose run kafkaconnect status influxdb-sink

Now use the kafka-avro-console-producer_ utility to produce Avro messages for the `foo` topic.
The Avro schema for the message value is specified using the `--property` command line option.
Note that because it runs inside the schema registry docker image, we need to use the internal broker port here:

.. _kafka-avro-console-producer: https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/kafka-commands.html#produce-avro-records

.. code-block:: bash

  docker-compose exec schema-registry kafka-avro-console-producer --bootstrap-server broker:29092 --topic foo --property value.schema='{"type":"record", "name":"foo", "fields":[{"name":"bar","type":"string"}, {"name":"baz","type":"float"}]}'
  {"bar": "John Doe", "baz": 1}
  {"bar": "John Doe", "baz": 2}
  Ctrl+D

Finally, you can query the results in InfluxDB, you should get an output like this:

.. code-block:: bash

  docker-compose exec influxdb influx -database mydb -execute "SELECT * FROM foo"
  name: foo
  time                bar      baz
  ----                ---      ---
  1611597963632953639 John Doe 1
  1611597964771771862 John Doe 1

You can inspect the connect service logs using:

.. code-block:: bash

   docker-compose logs connect


Avro records for both key and value
-----------------------------------

For producing Avro records for both key and value use:

.. code-block:: bash

  docker-compose exec schema-registry kafka-avro-console-producer --bootstrap-server broker:29092 --topic foo  --property parse.key=true --property key.schema='{"type":"record", "name":"id", "fields":[{"name":"id", "type":"int"}]}' --property value.schema='{"type":"record", "name":"foo", "fields":[{"name":"bar","type":"string",{"name":"baz","type":"float"}]}'
  {"id":1}	{"bar": "John Doe","baz": 1}
  Ctrl+D

Note that in this command we used <TAB> as the default separator for key and value, this can be changed with the `--property key.separator="<separator>"` option.

Recording arrays in InfluxDB
----------------------------

InfluxDB does not support array fields, the connector handles arrays in Avro by flattening them before writing to InfluxDB. The following command produce an Avro message with type array:

.. code-block:: bash

  docker-compose exec schema-registry kafka-avro-console-producer --bootstrap-server broker:29092 --topic foo --property value.schema='{"type":"record", "name":"foo", "fields":[{"name":"bar","type":"string"}, {"name":"baz","type":{"type":"array","items":"float"}}]}'
  {"bar": "John Doe","baz": [1,2,3]}
  Ctrl+D

which is stored in InfluxDB like:

.. code-block:: bash

  docker-compose exec influxdb influx -database mydb -execute "SELECT * FROM foo"
  name: foo
  time                bar      baz0 baz1 baz2
  ----                ---      ---- ---- ----
  1611707507555316950 John Doe 1    2    3


Resetting consumer group offsets
================================

When a sink connector is created, a consumer group keeps track of the offsets of each topic configured in the connector.
From the InfluxDB Sink connector created above, the following command list the consumer groups.

.. code-block:: bash

  docker-compose exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --list
  connect-influxdb-sink

The topic offset for the ``connect-influxdb-sink`` consumer group is shown using:

.. code-block:: bash

  docker-compose exec broker kafka-consumer-groups --bootstrap-server localhost:9092  --describe --offsets  --group connect-influxdb-sink

  GROUP                 TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                                             HOST            CLIENT-ID
  connect-influxdb-sink foo             0          1               1               0               connector-consumer-influxdb-sink-0-896a850d-4cbc-406c-a0c6-afcc7fb31da5 /192.168.80.6   connector-consumer-influxdb-sink-0

The log-end-offset is the offset of the last message sent to Kafka, and the current-offset is the offset of the last message consumed by the connector.
The difference is the consumer lag.
In the example, the connector is configured with only one topic ``foo``, and the only message produced was consumed by the connector.

It is possible to force the connector to consume the messages produced to the ``foo`` topic again by resetting the consumer group offsets.

The following commands will make the connector to write the messages to InfluxDB again, by resetting the consumer group offsets to the earliest offset available in Kafka.

First we check the consumer group state:

.. code-block:: bash

  docker-compose exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --group connect-influxdb-sink --describe --state

  GROUP                     COORDINATOR (ID)          ASSIGNMENT-STRATEGY  STATE           #MEMBERS
  connect-influxdb-sink     localhost:9092 (1)        range                Stable          1

To reset offsets wee need to change the consumer group state to ``Empty``.
To do that we delete the connector that is using the consumer group.

.. code-block:: bash

  docker-compose run kafkaconnect delete influxdb-sink

Now we reset the consumer group offsets:

.. code-block:: bash

  docker-compose exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --group connect-influxdb-sink --topic foo --reset-offsets --to-earliest --execute

  GROUP                          TOPIC                          PARTITION  NEW-OFFSET
  connect-influxdb-sink          foo                            0          0

And finally recreate the connector:

.. code-block:: bash

  docker-compose run kafkaconnect create influxdb-sink -d mydb foo

When deploying multiple InfluxDB Sink connectors consuming the same topics, a possible scenario is to configure one connector consuming the earliest offsets to recover historical data from Kafka into InfluxDB ("repairer" connector), and a second connector consuming the latest offsets to keep up with the current data in InfluxDB.
