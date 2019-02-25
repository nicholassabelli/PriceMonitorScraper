# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from urllib.parse import unquote
from price_monitor.items import Price, Product
from price_monitor.models import Availability, UniversalProductCode

class PriceMonitorPipeline(object):
    def process_item(self, item, spider):
        return item

class TagsPipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_TAGS):
            item[Product.KEY_TAGS] = item[Product.KEY_TAGS].split(',')
        
        return item

class BreadcrumbTagsPipeline(TagsPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_TAGS):
            item[Product.KEY_TAGS] = unquote(item[Product.KEY_TAGS]).split('/')

        return item

# class MetroBreadcrumbTagsPipeline(BreadcrumbTagsPipeline):
#     def process_item(self, item, spider):
#         if item.get(Product.KEY_TAGS):
#             item[Product.KEY_TAGS] = unquote(item[Product.KEY_TAGS]).split('/')

#         return item

class StripAmountPipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_CURRENT_PRICE).get(Price.KEY_AMOUNT):
            item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT] = item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT].strip('$')
        
        return item

class IGAStripAmountPipeline(StripAmountPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_CURRENT_PRICE).get(Price.KEY_AMOUNT):
            item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT] = item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT].strip('$')
            item[Product.KEY_AVAILABILITY] = Availability.IN_STOCK
        else:
            item[Product.KEY_AVAILABILITY] = Availability.OUT_OF_STOCK
        
        return item

class UniversalProductCodePipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        return item

class IGAUniversalProductCodePipeline(UniversalProductCodePipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_UPC):
            item[Product.KEY_UPC] = UniversalProductCode(item[Product.KEY_UPC].split('_')[1]).value
        
        return item