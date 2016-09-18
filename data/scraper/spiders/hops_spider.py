# -*- coding: utf-8 -*-
import scrapy
from scraper.items import HopsItem


class HopslistSpider(scrapy.Spider):
    name = "hopslist"
    allowed_domains = ["hopslist.com"]
    start_urls = (
        'http://www.hopslist.com/hops/',
    )

    def parse(self, response):
        # for href in response.xpath("//ul[@class='category-module']/li/h6/a/@href").extract():  # nopep8
        for href in response.xpath("//ul[@class='display-posts-listing']/li/a/@href").extract():  # nopep8
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_hops_contents)

    def parse_hops_contents(self, response):
        item = HopsItem()

        item[u'source'] = response.url
        item[u'source_id'] = item['source'].split('/')[-2]

        item[u'component'] = item['source'].split('/')[-3]
        name = response.xpath("//h1[@class='entry-title']/text()").extract()  # nopep8
        item[u'name'] = '_'.join(name)
        for entry in response.xpath('//table/tbody/tr'):
            category = entry.xpath('td[1]/text()').extract()
            data = entry.xpath('td[2]/text()').extract()
            cat_safe = ' '.join([c.strip() for c in category]).lower().strip()
            data_safe = ' '.join([d.strip() for d in data])
            if cat_safe:
                cat_safe = cat_safe.replace('?', '')
                cat_safe = cat_safe.replace(' ', '_')
                cat_safe = cat_safe.replace(' ', '-')
                if u'humulone' in cat_safe:
                    cat_safe = u'co_humulone_composition'
                if cat_safe == u'east_of_harvest':
                    cat_safe = u'ease_of_harvest'
                if cat_safe == u'alpha_acid\xa0composition':
                    cat_safe = u'alpha_acid_composition'
                item[cat_safe] = data_safe
        yield item
