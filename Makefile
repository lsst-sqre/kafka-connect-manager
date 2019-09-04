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

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

docker: install
	python setup.py sdist
	docker build --build-arg VERSION=$(VERSION) -t lsstsqre/kafka-connect-manager:build .

travis-docker-deploy:
	./bin/travis-docker-deploy.bash lsstsqre/kafka-connect-manager build

version:
	connect_manager --version

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .pytest_cache
