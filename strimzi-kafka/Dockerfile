# Build strimzi-kafka image with the influxdb connector plugin
FROM quay.io/strimzi/kafka:0.27.1-kafka-3.0.0
USER root:root
COPY kafka-connect-influxdb-3.0.1-2.5.0-all.jar /opt/kafka/plugins/
RUN chmod -R ag+w /opt/kafka/plugins
USER 1001
