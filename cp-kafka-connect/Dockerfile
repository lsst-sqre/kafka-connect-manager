ARG CONFLUENT_VERSION
FROM confluentinc/cp-kafka-connect:$CONFLUENT_VERSION
MAINTAINER afausti@lsst.org

# Add the InfluxDB Sink Connector
# Download kafka-connect-influxdb from
# https://github.com/lsst-sqre/stream-reactor/releases/tag/1.2.2-tickets-DM-21334

RUN mkdir -p /etc/landoop/jars/lib
COPY kafka-connect-influxdb-1.2.2-tickets-DM-21334.jar /etc/landoop/jars/lib
RUN chmod -R ag+w /etc/landoop/jars/lib
