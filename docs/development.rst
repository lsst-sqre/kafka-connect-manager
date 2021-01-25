#################
Development guide
#################

Development workflow
====================

Set up `kafka-connect-manager` for local development.

1. Clone the `kafka-connect-manager <https://github.com/lsst-sqre/kafka-connect-manager>`_ repo from GitHub:

.. code-block:: bash

  $ git clone https://github.com/lsst-sqre/kafka-connect-manager.git

2. Install your local copy into a virtualenv:

.. code-block:: bash

  $ cd kafka-connect-manager
  $ virtualenv -p Python3 venv
  $ source venv/bin/activate
  $ make update

3. Create a branch for local development:

.. code-block:: bash

  $ git checkout -b name-of-your-bugfix-or-feature

4. Check that your changes pass the linter and tests:

.. code-block:: bash

  $ tox -e lint typing py37

5. Commit your changes and push your branch to GitHub:

.. code-block:: bash

  $ git add .
  $ git commit -m "Your detailed description of your changes."
  $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.


Running locally with docker-compose
===================================

docker-compose_  provides the additional services you need to run kafka-connect-manager locally.

.. _docker-compose: https://github.com/lsst-sqre/kafka-connect-manager/blob/master/tests/docker-compose.yml

Start the kafka `broker`, `zookeeper` and `connect` services:

.. code-block:: bash

  cd kafka-connect-manager/tests
  docker-compose up broker zookeeper and connect -d

Example: Creating an instance of the influxdb-sink connector
------------------------------------------------------------

The following will create an instance of the influxdb-sink connector configured
to write three kafka topics `foo`, `bar` and `baz` to the `mydb` InfluxDB database.

.. code-block:: bash

  $ kafkaconnect create influxdb-sink --influxdb-url http://influxdb:8086 --database mydb foo bar baz
  Discoverying Kafka topics...
  Validation returned 0 error(s).
  Uploading influxdb-sink connector configuration...


The `create` command provides sensible defaults for the connector configuration. Use `--help` to see the available options for each connector.

You can inspect the connector configuration with the `config` command:

.. code-block:: bash

  $ kafkaconnect config influxdb-sink
  {
    "connect.influx.db": "mydb",
    "connect.influx.error.policy": "THROW",
    "connect.influx.kcql": "INSERT INTO foo SELECT * FROM foo WITHTIMESTAMP sys_time();INSERT INTO bar SELECT * FROM bar WITHTIMESTAMP sys_time();INSERT INTO baz SELECT * FROM baz WITHTIMESTAMP sys_time()",
    "connect.influx.max.retries": "10",
    "connect.influx.password": "",
    "connect.influx.retry.interval": "60000",
    "connect.influx.timestamp": "sys_time()",
    "connect.influx.url": "http://influxdb:8086",
    "connect.influx.username": "-",
    "connect.progress.enabled": "false",
    "connector.class": "com.datamountaineer.streamreactor.connect.influx.InfluxSinkConnector",
    "name": "influxdb-sink",
    "tasks.max": "1",
    "topics": "foo,bar,baz"
  }

You can check the status of the connector with the `status` command:

.. code-block:: bash

  $ kafkaconnect status influxdb-sink
  {
    "connector": {
        "state": "RUNNING",
        "worker_id": "connect:8083"
    },
    "name": "influxdb-sink",
    "tasks": [
        {
            "id": 0,
            "state": "RUNNING",
            "worker_id": "connect:8083"
        }
    ],
    "type": "sink"
}
