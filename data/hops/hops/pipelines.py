# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class HopsPipeline(object):

    def process_item(self, item, spider):
        filename = "{}.json".format(item['source'].split('/')[-1])
        with open(filename, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item
