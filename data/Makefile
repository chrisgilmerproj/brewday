#! /usr/bin/make 

VENV_DIR?=env
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);

.PHONY: help venv scrape_cereals scrape_hops scrape_yeast

help:  ## Print the help documentation
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(VENV_ACTIVATE): requirements.txt requirements-dev.txt
	test -f $@ || virtualenv --python=python2.7 $(VENV_DIR)
	$(WITH_VENV) pip install --no-deps -r requirements.txt
	$(WITH_VENV) pip install --no-deps -r requirements-dev.txt
	touch $@

venv: $(VENV_ACTIVATE)

scrape_cereals:  ## Scrape cereals data
	$(WITH_VENV) scrapy runspider scraper/spiders/cereals_spider.py

scrape_hops:  ## Scrape hops data
	$(WITH_VENV) scrapy runspider scraper/spiders/hops_spider.py

scrape_yeast:  ## Scrape yeast data
	$(WITH_VENV) scrapy runspider scraper/spiders/yeast_spider.py

default: help
