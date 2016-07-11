# -*- coding: utf-8 -*-
import scrapy
from scraper.items import YeastItem


class YeastlistSpider(scrapy.Spider):
    name = "yeastlist"
    allowed_domains = ["brewersfriend.com"]
    start_urls = (
        'http://www.brewersfriend.com/yeast-wyeast/',
        'http://www.brewersfriend.com/yeast-whitelabs/',
        'http://www.brewersfriend.com/yeast-fermentis/',
        'http://www.brewersfriend.com/yeast-danstar/',
        'http://www.brewersfriend.com/yeast-other/',
    )

    def parse(self, response):

        source = response.url
        man = response.xpath("//h2/text()").extract()[0]
        if 'by' in man:
            manufacturer = man.split(' by ')[-1]
        elif 'By' in man:
            manufacturer = man.split(' By ')[-1]
        for entry in response.xpath("//div[@class='post']/table/tbody/tr"):
            data = entry.xpath("td/span/text()").extract()
            if len(data) and data[0] != u'\n':
                item = YeastItem()
                item[u'name'] = data[0]
                item[u'source'] = source
                item[u'manufacturer'] = manufacturer
                item[u'yeast_id'] = data[1]
                item[u'attenuation'] = data[2]
                item[u'flocculation'] = data[3]
                item[u'optimum_temp'] = data[4].split()[0]
                item[u'alcohol_tolerance'] = data[5]
                yield item
