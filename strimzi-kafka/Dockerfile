# Build strimzi-kafka image with the influxdb connector plugin
FROM quay.io/strimzi/kafka:0.35.1-kafka-3.4.0
USER root:root
COPY kafka-connect-influxdb-3.0.1-timestampunit.jar /opt/kafka/plugins/
COPY confluentinc-kafka-connect-avro-converter-7.2.0 /opt/kafka/plugins/confluentinc-kafka-connect-avro-converter-7.2.0
COPY confluentinc-kafka-connect-jdbc-10.7.4.zip /opt/kafka/plugins/
RUN unzip /opt/kafka/plugins/confluentinc-kafka-connect-jdbc-10.7.4.zip -d /opt/kafka/plugins/
RUN rm /opt/kafka/plugins/confluentinc-kafka-connect-jdbc-10.7.4.zip
RUN chmod -R ag+w /opt/kafka/plugins
RUN ls /opt/kafka/plugins
USER 1001
