.PHONY: help cp-kafka-connect

# Version for the specific connectors
CONFLUENT_VERSION=5.5.2

# Version for cp-kafka-connect, go along with the version of
# kafka-connect-manager
VERSION=0.8.2-tickets-DM-21334

help:
	@echo "Make command reference"
	@echo "  make cp-kafka-connect ....... (make cp-kafka-connect docker image)"

cp-kafka-connect:
	docker build --build-arg CONFLUENT_VERSION=$(CONFLUENT_VERSION) \
							 -t lsstsqre/cp-kafka-connect:$(CONFLUENT_VERSION)-$(VERSION) .
	docker push lsstsqre/cp-kafka-connect:$(CONFLUENT_VERSION)-$(VERSION)
