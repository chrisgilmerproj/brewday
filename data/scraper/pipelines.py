# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os

from scraper.items import CerealsItem
from scraper.items import HopsItem

CEREALS_DIR = './cereals'
HOPS_DIR = './hops'


class CerealsPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, CerealsItem):
            return item
        filename = "{}.json".format(item['source'].split('/')[-1].split('.')[0])  # nopep8
        filepath = os.path.join(os.path.abspath(CEREALS_DIR), filename)
        with open(filepath, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item


class HopsPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, HopsItem):
            return item
        filename = "{}.json".format(item['source'].split('/')[-1])
        filepath = os.path.join(os.path.abspath(HOPS_DIR), filename)
        with open(filepath, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item
