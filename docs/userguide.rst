################################
How to run kafka-connect-manager
################################


Running locally with docker-compose
===================================

In this guide, we use ``docker-compose`` to illustrate how to run kafka-connect-manager. To run kafka-connect-manger on a Kubernetes environment see the :ref:`installation` section instead.

kafka-connect-manager `docker-compose configuration`_ includes services to run Confluent Kafka (zookeeper, broker and connect) and was based on `this example`_.

.. _docker-compose configuration: https://github.com/lsst-sqre/kafka-connect-manager/blob/master/tests/docker-compose.yaml
.. _this example: https://github.com/confluentinc/examples/blob/5.5.1-post/cp-all-in-one/docker-compose.yml

Clone the kafka-connect-manager repository:

.. code-block:: bash

  $ git clone https://github.com/lsst-sqre/kafka-connect-manager.git

Start the `zookeeper`, `broker` and `connect` services:

.. code-block:: bash

  cd tests
  docker-compose up zookeeper broker connect


On another terminal session, create a new Python virtual environment and install the kafkaconnect app locally:

.. code-block:: bash

  $ cd kafka-connect-manager
  $ virtualenv -p Python3 venv
  $ source venv/bin/activate
  $ make update

Using the kafkaconnect tool
===========================

See the available commands with the kafkaconnect tool:

.. code-block:: bash

  $ kafkaconnect --help


Example: Creating an influxdb-sink connector
--------------------------------------------

See the available configuration settings for the influxdb-sink connector with:

.. code-block:: bash

  $ kafkaconnect create influxdb-sink --help

The following will create an instance of the influxdb-sink connector configured
to write three kafka topics `t1`, `t2` and `t3` to the `mydb` InfluxDB database.

.. code-block:: bash

  $ kafkaconnect create influxdb-sink --database mydb t1 t2 t3
  Discoverying Kafka topics...
  Validation returned 0 error(s).
  Uploading influxdb-sink connector configuration...

  $ kafkaconnect config influxdb-sink
  {
    "connect.influx.db": "mydb",
    "connect.influx.error.policy": "THROW",
    "connect.influx.kcql": "INSERT INTO t1 SELECT * FROM t1 WITHTIMESTAMP sys_time();INSERT INTO t2 SELECT * FROM t2 WITHTIMESTAMP sys_time();INSERT INTO t3 SELECT * FROM t3 WITHTIMESTAMP sys_time()",
    "connect.influx.max.retries": "10",
    "connect.influx.password": "",
    "connect.influx.retry.interval": "60000",
    "connect.influx.timestamp": "sys_time()",
    "connect.influx.url": "http://localhost:8086",
    "connect.influx.username": "-",
    "connect.progress.enabled": "false",
    "connector.class": "com.datamountaineer.streamreactor.connect.influx.InfluxSinkConnector",
    "name": "influxdb-sink",
    "tasks.max": "1",
    "topics": "t1,t2,t3"
  }
