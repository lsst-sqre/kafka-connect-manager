FROM python:3.7-slim
MAINTAINER afausti@lsst.org
LABEL description="Python client for managing Confluent Kafka connectors" \
      name="lsstsqre/kafka-connect-manager"

USER root
RUN useradd -d /home/app -m app && \
    mkdir /dist && \
    pip install --upgrade pip

# Supply on CL as --build-arg VERSION=<version> (or run `make docker`).
ARG        VERSION="0.1.0"
LABEL      version=$VERSION
COPY       dist/kafka-connect-manager-$VERSION.tar.gz /dist
RUN        pip install /dist/kafka-connect-manager-$VERSION.tar.gz

USER app
WORKDIR /home/app

CMD [ "connect-manager", "--version" ]
