# -*- coding: utf-8 -*-

import logging, pymongo, re
from datetime import datetime
from scrapy.utils.project import get_project_settings
from price_monitor.items import (
    offer,
    product,
    product_data,
    store_item,
)
from price_monitor.models import (
    language,
)

class MongoDBPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings.get('MONGODB_SERVER'),
            settings.get('MONGODB_PORT'),
        )
        db = connection[settings.get('MONGODB_DB')]
        self.products_collection = db[settings.get('MONGODB_COLLECTION_PRODUCTS')]
        self.offers_collection = db[settings.get('MONGODB_COLLECTION_OFFERS')]
        self.stores_collection = db[settings.get('MONGODB_COLLECTION_STORES')]

    def process_item(self, item, spider):
        product_dictionary = dict(item)
    
        # TODO: Handle errors.

        # Extract sub dictionaries to new collections.
        offer_dictionary = product_dictionary.pop(
            product.Product.KEY_CURRENT_OFFER, 
            None,
        )
        store_dictionary = product_dictionary.pop(
            product.Product.KEY_STORE, 
            None,
        )
        product_data_dictionary = product_dictionary.pop(
            product.Product.KEY_PRODUCT_DATA, 
            None,
        )
        store_seller_key = list(product_data_dictionary.keys())[0]
        product_data_store_dictionary = product_data_dictionary.get(
            store_seller_key
        )
        supported_languages_dictionary = product_data_store_dictionary.get(
            product_data.ProductData.KEY_SUPPORTED_LANGUAGES
        )
        lang = list(
            supported_languages_dictionary.keys()
        )[0]

        # Add/fix datetime fields.
        self.__add_or_fix_datetime_field(
            offer_dictionary=offer_dictionary,
            product_data_store_dictionary=product_data_store_dictionary,
            product_dictionary=product_dictionary,
            store_dictionary=store_dictionary,
            supported_languages_dictionary=supported_languages_dictionary[lang],
        )

        self.__upsert_store(store_dictionary)

        insertProduct = False       
        product_found_by_store_and_number = None
        product_found_by_gtin = self.__find_product_found_by_gtin(product_dictionary) \
            if product_dictionary.get(product.Product.KEY_GTIN) else None

        if not product_found_by_gtin:
            product_found_by_store_and_number = \
                self.__find_product_by_model_number_and_brand(
                    model_number=product_dictionary[
                        product.Product.KEY_MODEL_NUMBER
                    ],
                    brand=product_dictionary[
                        product.Product.KEY_BRAND
                    ],
                )

            if not product_found_by_store_and_number:
                insertProduct = True 

        if insertProduct:
            product_dictionary[
                product.Product.KEY_PRODUCT_DATA
            ] = product_data_dictionary
            
            product_id = self.products_collection.insert(product_dictionary)
            logging.log(logging.INFO, "Added product to database!")
        else:
            product1 = product_found_by_gtin or product_found_by_store_and_number
            product_id = product1[product.Product.KEY_ID]
            product_data_store_seller_index = \
                    self.__create_product_data_dictionary_store_seller_index(
                        store_seller_key=store_seller_key,
                    )

            if not product1[product.Product.KEY_PRODUCT_DATA].get(store_seller_key):
                logging.info('Store data is  not set.')

                self.products_collection.update_one(
                    filter={
                        product.Product.KEY_ID: product1[
                            product.Product.KEY_ID
                        ],
                    }, 
                    update={
                        '$set': {
                            product_data_store_seller_index: \
                                product_data_dictionary[store_seller_key],
                            product.Product.KEY_UPDATED: product_dictionary[
                                product.Product.KEY_UPDATED
                            ]
                        },
                    },
                )
            elif not product1[product.Product.KEY_PRODUCT_DATA].get(store_seller_key).get(product_data.ProductData.KEY_SUPPORTED_LANGUAGES).get(lang):
                # Check if language is set.
                self.products_collection.update(
                    {
                        product.Product.KEY_ID: product1[product.Product.KEY_ID],
                    }, 
                    {
                        '$set':  {
                            product_data_store_seller_index + '.' + product_data.ProductData.KEY_NAME + '.' + lang: product_data_dictionary[store_seller_key][product_data.ProductData.KEY_NAME][lang],
                            product_data_store_seller_index + '.' + product_data.ProductData.KEY_DESCRIPTION  + '.' + lang: product_data_dictionary[store_seller_key][product_data.ProductData.KEY_DESCRIPTION][lang],
                            product_data_store_seller_index + '.' + product_data.ProductData.KEY_SUPPORTED_LANGUAGES  + '.' + lang: product_data_dictionary[store_seller_key][product_data.ProductData.KEY_SUPPORTED_LANGUAGES][lang],
                            product_data_store_seller_index + '.' + product_data.ProductData.KEY_UPDATED: product_data_dictionary[store_seller_key][product.Product.KEY_UPDATED],
                            product.Product.KEY_UPDATED: product_dictionary[
                                product.Product.KEY_UPDATED
                            ],
                        },
                    },
                )

                logging.log(logging.INFO, "Updated product, added a new language in product data in database!") # TODO: More descriptive messages, use variables.

        # logging.log(logging.INFO, "Updated product's product data in database!") 
        # TODO: Check if URL is the same.
        # TODO: Add new language to fields.
        # TODO: Add supported languages.

        offer_dictionary[offer.Offer.KEY_PRODUCT_ID] = product_id

        offer_id = self.offers_collection.insert(offer_dictionary)
        logging.log(logging.INFO, "Added offer to database!")
        
        return item

    def __is_product_data_set(self, subject, index): # TODO: No lookup required.
        return True if subject.get(index) else False

    def __is_language_set(self, subject, store_id, sold_by, language):
        # if lookup.get(f"{store_id} ({sold_by})") and lookup.get(ProductData.KEY_STORE_ID).get(f"{store_id} ({sold_by})").get(language):
        #     return True

        return False

    # def __get_model_number_index(self, store_seller_key):
    #     return product.Product.KEY_PRODUCT_DATA \
    #                 + '.' + store_seller_key \
    #                 + '.' + product_data.ProductData.KEY_MODEL_NUMBER

    # def __get_sku_index(self, store_seller_key):
    #     return product.Product.KEY_PRODUCT_DATA \
    #                 + '.' + store_seller_key \
    #                 + '.' + product_data.ProductData.KEY_SKU 

    def __create_product_data_dictionary_store_seller_index(
        self, 
        store_seller_key,
    ):
        return product.Product.KEY_PRODUCT_DATA \
                    + '.' + store_seller_key

    def __find_product_found_by_gtin(self, product_dictionary):
        return self.products_collection.find_one({
            product.Product.KEY_GTIN: product_dictionary[
                product.Product.KEY_GTIN
            ]
        })
    
    def __find_product_by_model_number_and_brand(
        self, 
        model_number, 
        brand,
    ):
        brand_regex = re.compile(f'^{brand}$', re.IGNORECASE)
        
        return self.products_collection.find_one(
            {
                '$and': [
                    {
                        product.Product.KEY_MODEL_NUMBER: model_number
                    },
                    {
                        product.Product.KEY_BRAND: brand_regex
                    }
                ]
            }
        )
    
    def __add_or_fix_datetime_field(
        self,
        offer_dictionary,
        product_data_store_dictionary,
        product_dictionary,
        store_dictionary,
        supported_languages_dictionary,
    ):
        dictionaries = [
            offer_dictionary,
            product_data_store_dictionary,
            product_dictionary,
            store_dictionary,
            supported_languages_dictionary,
        ]

        now = datetime.utcnow()
        datetime_indexes = [
            'created',
            'updated',
        ]

        for dictionary in dictionaries:
            for datetime_index in datetime_indexes:
                dictionary[datetime_index] = now

    def __upsert_store(self, store_dictionary):
        # nUpserted
        # writeConcernError
        return self.stores_collection.update_one(
            filter={
                store_item.StoreItem.KEY_ID: store_dictionary[
                    store_item.StoreItem.KEY_ID
                ]
            },
            update={
                '$setOnInsert': store_dictionary,
            },
            upsert=True,
        )
        # logging.log(logging.INFO, "Added store to database!")