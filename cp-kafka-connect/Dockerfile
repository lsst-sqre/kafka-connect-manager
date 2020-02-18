ARG CONFLUENT_VERSION
FROM confluentinc/cp-kafka-connect:$CONFLUENT_VERSION
MAINTAINER afausti@lsst.org

# Add the InfluxDB Sink Connector
# Download or build the connector from from https://github.com/llensesio/stream-reactor
ARG STREAM_REACTOR_VERSION
RUN mkdir -p /etc/landoop/jars/lib
COPY kafka-connect-influxdb-$STREAM_REACTOR_VERSION-2.1.0-all.jar /etc/landoop/jars/lib
RUN chmod -R ag+w /etc/landoop/jars/lib

# Add the Oracle JDBC driver for the Confluent JDBC Sink Connector
# Download the Oracle JDBC driver (ojdbc8.jar) from
# https://www.oracle.com/technetwork/database/application-development/jdbc/downloads/index.html
# COPY ./ojdbc8.jar /usr/share/java/kafka-connect-jdbc/

# Add the Replicator Connector
# Download the corresponding version of the Replicator connector from
# https://www.confluent.io/hub/confluentinc/kafka-connect-replicator
RUN mkdir -p /usr/share/java/kafka-connect-replicator
COPY confluentinc-kafka-connect-replicator-$CONFLUENT_VERSION/lib/* /usr/share/java/kafka-connect-replicator/
