# Build strimzi-kafka image with the influxdb connector plugin
FROM quay.io/strimzi/kafka:0.29.0-kafka-3.1.1
USER root:root
COPY kafka-connect-influxdb-3.0.1-timestampunit.jar /opt/kafka/plugins/
RUN chmod -R ag+w /opt/kafka/plugins
USER 1001
