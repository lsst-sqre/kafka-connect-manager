.PHONY: help install test image travis-docker-deploy version

VERSION=$(shell connect_manager --version)

help:
	@echo "Make command reference"
	@echo "  make install ..... (install app for development)"
	@echo "  make test ........ (run unit tests pytest)"
	@echo "  make docker ....... (make tagged Docker image)"
	@echo "  make travis-docker-deploy (push image to Docker Hub from Travis CI)"
	@echo "  make version ..... (print the app version)"


develop:
	python setup.py develop

test:
	python setup.py test

install:
	python setup.py install

docker: install
	python setup.py sdist
	docker build --build-arg VERSION=$(VERSION) -t lsstsqre/cp-kafka-connect-manager:build .

travis-docker-deploy:
	./bin/travis-docker-deploy.bash lsstsqre/cp-kafka-connect-manager build

version:
	connect_manager --version
