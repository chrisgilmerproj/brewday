# -*- coding: utf-8 -*-
import scrapy

from scraper.items import CerealsItem


class BeerSmithSpider(scrapy.Spider):
    name = "beersmith"
    allowed_domains = ["beersmith.com"]
    start_urls = (
        'http://beersmith.com/grain-list/',
    )

    def parse(self, response):
        for href in response.xpath('//table[@class="ms-list4-main"]/tbody/tr/td/a/@href').extract():  # nopep8
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_cereals_contents)

    def parse_cereals_contents(self, response):
        item = CerealsItem()

        item[u'source'] = response.url
        source_id = item['source'].split('/')[-1].split('.')[0].split('_')[-1]
        item[u'source_id'] = source_id

        name = response.xpath('//h2/text()').extract()[0]
        item[u'name'] = name
        notes = response.xpath("//body/center/table/tbody/tr/td/text()").extract()  # nopep8
        item[u'notes'] = ' '.join(notes).strip()

        for entry in response.xpath('//table/tbody/tr/td/table/tbody/tr/td'):
            category = entry.xpath('b/text()').extract()
            data = entry.xpath('text()').extract()
            cat_safe = ' '.join([c.strip() for c in category]).lower().strip()
            data_safe = ' '.join([d.strip() for d in data])
            if cat_safe:
                cat_safe = cat_safe[:-1]
                cat_safe = cat_safe.replace('/', '_')
                cat_safe = cat_safe.replace(' ', '_')
                if cat_safe == u'type':
                    cat_safe = u'cereal_type'
                item[cat_safe] = data_safe
        yield item
