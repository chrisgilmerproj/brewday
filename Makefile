#! /usr/bin/make 

PACKAGE_NAME=brew

VENV_DIR?=.venv
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);

TEST_OUTPUT?=nosetests.xml
COVERAGE_OUTPUT?=coverage.xml

.PHONY: help venv setup clean teardown lint test package

help:  ## Print the help documentation
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(VENV_ACTIVATE): requirements.txt requirements-dev.txt
	test -f $@ || virtualenv --python=python2.7 $(VENV_DIR)
	$(WITH_VENV) pip install --no-deps -r requirements.txt
	$(WITH_VENV) pip install --no-deps -r requirements-dev.txt
	touch $@

venv: $(VENV_ACTIVATE)

setup: venv

clean: ## Clean the library and test files
	python setup.py clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf */__pycache__/
	rm -f MANIFEST
	rm -f $(TEST_OUTPUT)
	coverage erase
	rm -f $(COVERAGE_OUTPUT)
	find ./ -type f -name '*.pyc' -delete

teardown: ## Remove all virtualenv files
	rm -rf $(VENV_DIR)/

lint: venv ## Run linting tests
	$(WITH_VENV) flake8 $(PACKAGE_NAME)/

test: venv ## Run unit tests
	$(WITH_VENV) tox

package:  ## Create the python package
	python setup.py sdist

install:  ## Install the python package
	$(WITH_VENV) python setup.py install

default: help
