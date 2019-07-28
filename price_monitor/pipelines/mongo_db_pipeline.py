# -*- coding: utf-8 -*-

import logging, pymongo
from datetime import datetime
from scrapy.conf import settings

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