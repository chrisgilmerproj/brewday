# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os

HOPS_DIR = './hops'


class HopsPipeline(object):

    def process_item(self, item, spider):
        filename = "{}.json".format(item['source'].split('/')[-1])
        filepath = os.path.join(os.path.abspath(HOPS_DIR), filename)
        with open(filepath, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item
