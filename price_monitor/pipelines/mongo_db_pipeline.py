# -*- coding: utf-8 -*-

import logging, pymongo
from datetime import datetime
from scrapy.conf import settings
from price_monitor.items import Offer, Product, ProductData, ProductDataLookup, Store

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
        product_dictionary = dict(item)
    
        # Extract sub dictionaries to new collection.
        offer_dictionary = product_dictionary.pop(Product.KEY_CURRENT_OFFER, None)
        store_dictionary = product_dictionary.pop(Product.KEY_STORE, None)
        product_data_dictionary = product_dictionary.pop(Product.KEY_PRODUCT_DATA_RAW, None)

        # Add/fix datetime fields.
        now = datetime.utcnow()
        product_dictionary[Product.KEY_CREATED] = now
        product_dictionary[Product.KEY_UPDATED] = now
        store_dictionary[Store.KEY_CREATED] = now
        store_dictionary[Store.KEY_UPDATED] = now

        # TODO: Handle errors.

        if not self.stores_collection.find_one({Store.KEY_ID: store_dictionary[Store.KEY_ID]}):
            store_id = self.stores_collection.insert(store_dictionary)
            logging.log(logging.INFO, "Added store to database!")

        insertProduct = False       
        product_by_model_number_and_store = None
        product_by_gtin = self.products_collection.find_one({Product.KEY_UPC: product_dictionary[Product.KEY_UPC]}) if product_dictionary.get(Product.KEY_UPC) else None

        if not product_by_gtin:
            product_by_model_number_and_store = self.products_collection.find_one({
                Product.KEY_PRODUCT_DATA + '.' + ProductData.KEY_MODEL_NUMBER: product_data_dictionary[ProductData.KEY_MODEL_NUMBER],
                Product.KEY_PRODUCT_DATA + '.' + ProductData.KEY_STORE_ID: store_dictionary[Store.KEY_ID],
            })

            if not product_by_model_number_and_store:
                insertProduct = True 

        if insertProduct:
            product_data_dictionary[ProductData.KEY_STORE_ID] = store_dictionary[Store.KEY_ID]
            product_dictionary[Product.KEY_PRODUCT_DATA] = [product_data_dictionary]
            
            product_id = self.products_collection.insert(product_dictionary)
            logging.log(logging.INFO, "Added product to database!")
        else:
            product = product_by_gtin or product_by_model_number_and_store
            product_id = product[Product.KEY_ID]

            # Check if store data is set.
            if not self.__isProductDataSet(product[Product.KEY_PRODUCT_DATA], store_dictionary[Store.KEY_ID], product_data_dictionary[ProductData.KEY_SOLD_BY]):
                self.products_collection.update(
                    {
                        Product.KEY_ID: product[Product.KEY_ID],
                    }, 
                    {
                        '$push': {
                            Product.KEY_PRODUCT_DATA: product_data_dictionary,
                        }
                    }
                )

                logging.log(logging.INFO, "Updated product's product data in database!")

            # TODO: Check if URL is the same.


            # Check if language is set.
            if not self.__isLanguageSet(product[Product.KEY_PRODUCT_DATA], store_dictionary[Store.KEY_ID], product_data_dictionary[ProductData.KEY_SOLD_BY], 'fr'): # TODO: Language.
                self.products_collection.update(
                    {
                        Product.KEY_ID: product[Product.KEY_ID],
                        Product.KEY_PRODUCT_DATA + '.' + ProductData.KEY_STORE_ID: product_data_dictionary[ProductData.KEY_STORE_ID],
                    }, 
                    {
                        '$push':  {
                            Product.KEY_PRODUCT_DATA + '.$.' + ProductData.KEY_NAME: product_data_dictionary[ProductData.KEY_NAME][0],
                            Product.KEY_PRODUCT_DATA + '.$.' + ProductData.KEY_DESCRIPTION: product_data_dictionary[ProductData.KEY_DESCRIPTION][0],
                        }
                    }
                )

                logging.log(logging.INFO, "Updated product, added a new language in product data in database!") # TODO: More descriptive messages, use variables.

        offer_dictionary[Offer.KEY_PRODUCT_ID] = product_id
        offer_dictionary[Offer.KEY_DATETIME] = datetime.fromisoformat(offer_dictionary['datetime'])
        offer_dictionary[Offer.KEY_CREATED] = now
        offer_dictionary[Offer.KEY_UPDATED] = now

        offer_id = self.offers_collection.insert(offer_dictionary)
        logging.log(logging.INFO, "Added offer to database!")
        
        return item

    def __isProductDataSet(self, lookup, store_id, sold_by):
        # if lookup.get(ProductData.KEY_STORE_ID).get(f"{store_id} ({sold_by})"):
        #     return True

        return False

    def __isLanguageSet(self, lookup, store_id, sold_by, language):
        # if lookup.get(f"{store_id} ({sold_by})") and lookup.get(ProductData.KEY_STORE_ID).get(f"{store_id} ({sold_by})").get(language):
        #     return True

        return False