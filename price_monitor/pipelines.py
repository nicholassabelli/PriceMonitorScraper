# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PriceMonitorPipeline(object):
    def process_item(self, item, spider):
        return item

class BestBuyTagsPipeline(object):
    def process_item(self, item, spider):
        if item['tags']:
            item['tags'] = item['tags'].split(',')
            return item