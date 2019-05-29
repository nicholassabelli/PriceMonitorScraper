# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo

from datetime import datetime
from urllib.parse import unquote
from price_monitor.items import Price, Product
from price_monitor.models import Availability, UniversalProductCode
from scrapy.conf import settings
from scrapy.exceptions import DropItem

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

            for x in ['', 'en', 'online_grocery', 'browse', 'in_the_community']:
                if item.get(x):
                    item.remove(x)

        return item

class StripAmountPipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_CURRENT_PRICE) and item.get(Product.KEY_CURRENT_PRICE).get(Price.KEY_AMOUNT):
            item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT] = float(item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT].strip('$'))
        
        return item

class IGAStripAmountPipeline(StripAmountPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_CURRENT_PRICE) and item.get(Product.KEY_CURRENT_PRICE).get(Price.KEY_AMOUNT):
            item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT] = float(item[Product.KEY_CURRENT_PRICE][Price.KEY_AMOUNT].strip('$'))
            item[Product.KEY_AVAILABILITY] = Availability.IN_STOCK.value
        else:
            item[Product.KEY_AVAILABILITY] = Availability.OUT_OF_STOCK.value
        
        return item

class UniversalProductCodePipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        return item

class IGAUniversalProductCodePipeline(UniversalProductCodePipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_UPC):
            item[Product.KEY_UPC] = UniversalProductCode(item[Product.KEY_UPC].split('_')[1]).value
        
        return item

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.products_collection = db[settings['MONGODB_COLLECTION_PRODUCTS']]
        self.prices_collection = db[settings['MONGODB_COLLECTION_PRICES']]

    def process_item(self, item, spider):
        prodDict = dict(item)
    
        # Extract price to new collection.
        priceDict = prodDict.pop('current_price', None)

        # Add/fix datetime fields.
        now = datetime.utcnow()
        prodDict['created'] = now
        prodDict['updated'] = now
        priceDict['datetime'] = datetime.fromisoformat(priceDict['datetime'])

        # TODO: Handle errors.

        self.products_collection.insert(prodDict)
        logging.log(logging.INFO, "Added to item database!")
        self.prices_collection.insert(priceDict)
        logging.log(logging.INFO, "Added to item database!")
        return item