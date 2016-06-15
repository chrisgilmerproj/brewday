# Beer Data

The beer data is split into four sections: Cereals, Hops, Water, and Yeast.
The data is provided in `*.ini` files, one file per data item.  Each item
should have a `[default]` section with a `name` parameter.  That parameter
should be identical to the name of the file, using underscores instead of
spaces or dashes.

An example for Cereals is American Pale 2-row.  The file name should be
`american_pale_2_row.ini` and the default name should be
`name = american pale 2-row`.

# Scraper

Using the python project Scrapy the data is collected from publicly available
websites where possible.  Try to ensure that the source is always listed in
any files scraped from websites.  Permission should always be asked for to
ensure there is no copyright problems.

## Running the scraper

``sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ scrapy runspider scraper/spiders/hops_spider.py
$ scrapy runspider scraper/spiders/cereals_spider.py
```

# Sources

## Cereals

- http://beersmith.com/grain-list/

## Hops

- http://www.hopslist.com/
