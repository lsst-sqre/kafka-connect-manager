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

The connector supports Avro type array, it extracts the elements of the array into individual fields in InfluxDB of the same type:

.. code-block:: bash

  docker-compose exec schema-registry kafka-avro-console-producer --bootstrap-server broker:29092 --topic foo --property value.schema='{"type":"record", "name":"foo", "fields":[{"name":"bar","type":"string"}, {"name":"baz","type":{"type":"array","items":"float"}}]}'
  {"bar": "John Doe","baz": [1,2,3]}
  Ctrl+D

which in InfluxDB is stored like:

.. code-block:: bash

  docker-compose exec influxdb influx -database mydb -execute "SELECT * FROM foo"
  name: foo
  time                bar      baz0 baz1 baz2
  ----                ---      ---- ---- ----
  1611707507555316950 John Doe 1    2    3
