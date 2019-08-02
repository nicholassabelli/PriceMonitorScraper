# -*- coding: utf-8 -*-

import logging, pymongo
from datetime import datetime
from scrapy.conf import settings
from price_monitor.items import Offer, Product, Store

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.products_collection = db[settings['MONGODB_COLLECTION_PRODUCTS']]
        self.offers_collection = db[settings['MONGODB_COLLECTION_OFFERS']]
        self.stores_collection = db[settings['MONGODB_COLLECTION_STORES']]

    def process_item(self, item, spider):
        prodDict = dict(item)
    
        # Extract price to new collection.
        offerDict = prodDict.pop('current_price', None)
        storeDict = prodDict.pop('store', None)

        # Add/fix datetime fields.
        now = datetime.utcnow()
        prodDict['created'] = now
        prodDict['updated'] = now
        storeDict['created'] = now
        storeDict['updated'] = now

        # TODO: Handle errors.

        if not self.stores_collection.find_one({Store.KEY_ID: storeDict[Store.KEY_ID]}):
            store_id = self.stores_collection.insert(storeDict)
            logging.log(logging.INFO, "Added to item database!")


        insertProduct = False       
        product_by_model_number_and_store = None
        product_by_gtin = self.products_collection.find_one({Product.KEY_UPC: prodDict[Product.KEY_UPC]}) if prodDict.get(Product.KEY_UPC) and prodDict[Product.KEY_UPC] else None

        if not product_by_gtin:
            product_by_model_number_and_store = self.products_collection.find_one({
                Product.KEY_MODEL_NUMBER: prodDict[Product.KEY_MODEL_NUMBER],
                Product.KEY_STORE_ID: storeDict[Store.KEY_ID], # TODO: Fix.
            })

            if not product_by_model_number_and_store:
                insertProduct = True 

        if insertProduct:
            prodDict[Product.KEY_STORE_ID] = storeDict[Store.KEY_ID]
            product_id = self.products_collection.insert(prodDict)
            logging.log(logging.INFO, "Added to item database!")
        else:
            product = product_by_gtin or product_by_model_number_and_store
            product_id = product[Product.KEY_ID]
            # TODO: Check if store data is set.
            # TODO: Check if language is set.
            pass

        offerDict[Offer.KEY_PRODUCT_ID] = product_id
        offerDict['datetime'] = datetime.fromisoformat(offerDict['datetime'])
        offerDict['created'] = now
        offerDict['updated'] = now

        offer_id = self.offers_collection.insert(offerDict)
        logging.log(logging.INFO, "Added to item database!")
        
        return item