FROM python:3.7.3
MAINTAINER afausti@lsst.org
LABEL description="Python client for managing Confluent Kafka connectors" \
      name="lsstsqre/cp-kafka-connect-manager"

USER root
RUN useradd -d /home/app -m app && \
    mkdir /dist && \
    pip install --upgrade pip

# Supply on CL as --build-arg VERSION=<version> (or run `make image`).
ARG        VERSION="0.1.0"
LABEL      version=$VERSION
COPY       dist/cp-kafka-connect-manager-$VERSION.tar.gz /dist
RUN        pip install /dist/cp-kafka-connect-manager-$VERSION.tar.gz

USER app
WORKDIR /home/app

CMD [ "connect-manager", "--version" ]
