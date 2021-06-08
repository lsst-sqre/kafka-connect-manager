ARG CONFLUENT_VERSION
FROM confluentinc/cp-kafka-connect:$CONFLUENT_VERSION
MAINTAINER afausti@lsst.org

# Add the InfluxDB Sink Connector
# Download kafka-connect-influxdb from
# https://github.com/lsst-sqre/stream-reactor/releases/tag/2.1.3-array-support

RUN mkdir -p /etc/landoop/jars/lib
COPY kafka-connect-influxdb-2.1.3-2.5.0-all.jar /etc/landoop/jars/lib
RUN chmod -R ag+w /etc/landoop/jars/lib
