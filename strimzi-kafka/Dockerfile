# Build strimzi-kafka image with the influxdb connector plugin
FROM quay.io/strimzi/kafka:0.34.0-kafka-3.3.1
USER root:root
COPY kafka-connect-influxdb-3.0.1-timestampunit.jar /opt/kafka/plugins/
COPY confluentinc-kafka-connect-avro-converter-7.2.0 /opt/kafka/plugins/confluentinc-kafka-connect-avro-converter-7.2.0
RUN chmod -R ag+w /opt/kafka/plugins
RUN ls /opt/kafka/plugins
USER 1001
