# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os

from scraper.items import CerealsItem
from scraper.items import HopsItem
from scraper.items import YeastItem

CEREALS_DIR = './cereals'
HOPS_DIR = './hops'
YEAST_DIR = './yeast'


class CerealsPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, CerealsItem):
            return item
        filename = item['name'].lower().replace(" ", "_")
        filename = filename.replace(",", "")
        filename = filename.replace("(", "")
        filename = filename.replace(")", "")
        filename = filename.replace("/", "_")
        filename = filename.replace("-", "_")
        filename = filename.replace("___", "_")
        filename = filename.replace("__", "_")
        filename = filename.replace("_-", "_")
        filename = "{}.json".format(filename)
        filepath = os.path.join(os.path.abspath(CEREALS_DIR), filename)
        item[u'color'] = float(item['color'][:-4])
        item[u'ppg'] = round((float(item['potential'][:-3]) - 1.0) * 1000, 1)
        with open(filepath, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item


class HopsPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, HopsItem):
            return item
        filename = item['source_id'].lower().replace(" ", "_")
        filename = filename.replace("(", "")
        filename = filename.replace(")", "")
        filename = filename.replace("'", "")
        filename = filename.replace("-", "_")
        filename = "{}.json".format(filename)
        filepath = os.path.join(os.path.abspath(HOPS_DIR), filename)
        if item[u'alpha_acid_composition']:
            item[u'percent_alpha_acids'] = round(float(item['alpha_acid_composition'].split('-')[0].split('%')[0]) / 100., 3)  # nopep8
        with open(filepath, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item


class YeastPipeline(object):
    ATTENUATION = {
        'NA': '0%',
        '-': '0%',
        'Low': '72%',
        'Medium': '75%',
        'Med-High': '76-77%',
        'Medium-High': '76-77%',
        'High': '78%',
        'Very High': '80%',
    }

    def process_item(self, item, spider):
        if not isinstance(item, YeastItem):
            return item
        if item[u'attenuation'] in self.ATTENUATION:
            item[u'attenuation'] = self.ATTENUATION[item[u'attenuation']]
        item[u'attenuation'] = item[u'attenuation'].replace("<", "")
        item[u'attenuation'] = item[u'attenuation'].replace(">", "")
        item[u'attenuation'] = item[u'attenuation'].replace("%", "")
        item[u'attenuation'] = item[u'attenuation'].split('-')
        item[u'attenuation'] = [float(att) / 100. for att in item[u'attenuation']]  # nopep8

        item[u'name'] = item[u'name'].replace('\u2013', '-')

        if 'yeast_id' in item:
            identifier = item['yeast_id'].lower()
        else:
            identifier = item['name'].lower()
        filename = '{}_{}'.format(item['manufacturer'].lower(),
                                  identifier)
        filename = filename.replace(" ", "_")
        filename = filename.replace("-", "_")
        filename = filename.replace("/", "_")
        filename = "{}.json".format(filename)
        filepath = os.path.join(os.path.abspath(YEAST_DIR), filename)
        with open(filepath, 'wb') as f:
            line = json.dumps(dict(item))
            f.write(line)
        return item
