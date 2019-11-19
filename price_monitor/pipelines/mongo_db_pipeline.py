# -*- coding: utf-8 -*-

import logging, pymongo
from datetime import datetime
from scrapy.conf import settings
from price_monitor.items import (
    offer,
    product,
    product_data,
    store_item
)
from price_monitor.models import (
    language
)

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
        offer_dictionary = product_dictionary.pop(
            product.Product.KEY_CURRENT_OFFER, 
            None
        )
        store_dictionary = product_dictionary.pop(
            product.Product.KEY_STORE, 
            None
        )
        product_data_dictionary = product_dictionary.pop(
            product.Product.KEY_PRODUCT_DATA, 
            None
        )

        # TODO: Handle errors.
        product_data_store_index = list(product_data_dictionary.keys())[0]

        # Add/fix datetime fields.
        self.__add_or_fix_datetime_field(
            offer_dictionary=offer_dictionary,
            product_data_store_dictionary=product_data_dictionary[
                product_data_store_index
            ],
            product_dictionary=product_dictionary,
            store_dictionary=store_dictionary,
            supported_languages_dictionary=product_data_dictionary \
                [product_data_store_index] \
                [product_data.ProductData.KEY_SUPPORTED_LANGUAGES],
        )

        self.__upsert_store(store_dictionary)
        # self.stores_collection.update(
        #     {
        #         store_item.StoreItem.KEY_ID: store_dictionary[
        #             store_item.StoreItem.KEY_ID
        #         ]
        #     },
        #     {
        #         store_dictionary
        #     },
        #     {
        #         'upsert': True
        #     }
        # )

        # if not self.stores_collection.find_one({
        #     store_item.StoreItem.KEY_ID: store_dictionary[
        #         store_item.StoreItem.KEY_ID
        #     ]
        # }):
        #     store_id = self.stores_collection.insert(store_dictionary)
        #     logging.log(logging.INFO, "Added store to database!")

        insertProduct = False       
        product_by_store_and_number = None
        product_by_gtin = self.__find_product_by_gtin(product_dictionary) \
            if product_dictionary.get(product.Product.KEY_GTIN) else None

        if not product_by_gtin:
            product_by_store_and_number = \
                self.__find_product_by_store_and_number(
                    product_data_store_index=product_data_store_index,
                    product_data_dictionary=product_data_dictionary,
                    store_dictionary=store_dictionary
                )

            if not product_by_store_and_number:
                insertProduct = True 

        if insertProduct:
            product_dictionary[
                product.Product.KEY_PRODUCT_DATA
            ] = product_data_dictionary
            
            product_id = self.products_collection.insert(product_dictionary)
            logging.log(logging.INFO, "Added product to database!")
        else:
            product1 = product_by_gtin or product_by_store_and_number
            product_id = product1[product.Product.KEY_ID]

            # TODO: upsert, setOnInsert.
            # Check if store data is set.
            # self.__upsert_product_data(
            #     product1,
            #     product_data_store_index,
            #     product_data_dictionary
            # )

            if not self.__is_product_data_set(
                subject=product1[product.Product.KEY_PRODUCT_DATA], 
                index=product_data_store_index,
            ):
                logging.info('Store data is set.')
                self.products_collection.update(
                    {
                        product.Product.KEY_ID: \
                            product1[product.Product.KEY_ID],
                    }, 
                    {
                        '$push': {
                            product.Product.KEY_PRODUCT_DATA: \
                                product_data_dictionary,
                        }
                    }
                )

        #         logging.log(logging.INFO, "Updated product's product data in database!")

        #     # TODO: Check if URL is the same.

        #     # Check if language is set.
        #     if not self.__isLanguageSet(product1[product.Product.KEY_PRODUCT_DATA], store_dictionary[store_item.StoreItem.KEY_ID], product_data_dictionary[product_data.ProductData.KEY_SOLD_BY], 'fr'): # TODO: Language.
        #         self.products_collection.update(
        #             {
        #                 product.Product.KEY_ID: product1[product.Product.KEY_ID],
        #                 product.Product.KEY_PRODUCT_DATA + '.' + product_data.ProductData.KEY_STORE_ID: product_data_dictionary[product_data.ProductData.KEY_STORE_ID],
        #             }, 
        #             {
        #                 '$push':  {
        #                     product.Product.KEY_PRODUCT_DATA + '.$.' + product_data.ProductData.KEY_NAME: product_data_dictionary[product_data.ProductData.KEY_NAME][0],
        #                     product.Product.KEY_PRODUCT_DATA + '.$.' + product_data.ProductData.KEY_DESCRIPTION: product_data_dictionary[product_data.ProductData.KEY_DESCRIPTION][0],
        #                 }
        #             }
        #         )

        #         logging.log(logging.INFO, "Updated product, added a new language in product data in database!") # TODO: More descriptive messages, use variables.

        # TODO: Add new language to fields.
        # TODO: Add supported languages.
        

        offer_dictionary[offer.Offer.KEY_PRODUCT_ID] = product_id
        offer_dictionary[offer.Offer.KEY_DATETIME] = datetime.fromisoformat(
            offer_dictionary['datetime']
        )

        offer_id = self.offers_collection.insert(offer_dictionary)
        logging.log(logging.INFO, "Added offer to database!")
        
        return item

    def __is_product_data_set(self, subject, index): # TODO: No lookup required.
        return True if (subject.get(index)) else False
        # return self.products_collection.find_one({
        #     product.Product.KEY_PRODUCT_DATA \
        #     + '.' + product_data_store_index: { 
        #         '$exists': True 
        #     }
        # })

    def __is_language_set(self, subject, store_id, sold_by, language):
        # if lookup.get(f"{store_id} ({sold_by})") and lookup.get(ProductData.KEY_STORE_ID).get(f"{store_id} ({sold_by})").get(language):
        #     return True

        return False

    def __get_model_number_index(self, product_data_store_index):
        return product.Product.KEY_PRODUCT_DATA \
                    + '.' + product_data_store_index \
                    + '.' + product_data.ProductData.KEY_MODEL_NUMBER

    def __get_sku_index(self, product_data_store_index):
        return product.Product.KEY_PRODUCT_DATA \
                    + '.' + product_data_store_index \
                    + '.' + product_data.ProductData.KEY_SKU 

    def __get_store_id_index(self, product_data_store_index):
        return product.Product.KEY_PRODUCT_DATA \
                    + '.' + product_data_store_index \
                    + '.' + product_data.ProductData.KEY_STORE_ID 
    
    def __find_product_by_gtin(self, product_dictionary):
        return self.products_collection.find_one({
            product.Product.KEY_GTIN: product_dictionary[
                product.Product.KEY_GTIN
            ]
        })
    
    def __find_product_by_store_and_number(
        self, 
        product_data_store_index,
        product_data_dictionary, 
        store_dictionary
    ):
        model_number_index = self.__get_model_number_index(
            product_data_store_index
        )
        sku_index = self.__get_sku_index(product_data_store_index)
        store_id_index = self.__get_store_id_index(product_data_store_index)
        
        return self.products_collection.find_one(
            {
                '$and': [
                    {
                        store_id_index: store_dictionary[
                            store_item.StoreItem.KEY_ID
                        ]
                    },
                    {
                        '$or': [
                            {
                                model_number_index: product_data_dictionary \
                                    [product_data_store_index] \
                                    [product_data.ProductData.KEY_MODEL_NUMBER]
                            },
                            {
                                sku_index: product_data_dictionary \
                                    [product_data_store_index] \
                                    [product_data.ProductData.KEY_SKU]
                            },
                        ]
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
        supported_languages_dictionary
    ):
        dictionaries = [
            offer_dictionary,
            product_data_store_dictionary,
            product_dictionary,
            store_dictionary,
        ]

        # TODO: Add index to item to avoid this loop.
        # Add the supported lang dict to the array of dicts to fix.
        for lang in language.Language:
            x = supported_languages_dictionary.get(lang.value)

            if x is not None:
                dictionaries.append(supported_languages_dictionary[
                    lang.value
                ])

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
                '$setOnInsert': store_dictionary
            },
            upsert=True
        )
        # logging.log(logging.INFO, "Added store to database!")

    # def __upsert_product_data(
    #     self, 
    #     product_item,
    #     product_data_store_index,
    #     product_data_dictionary
    # ):
    #     # nUpserted
    #     # writeConcernError
    #     return self.products_collection.update_one(
    #         filter={
    #             product.Product.KEY_ID: product_item[product.Product.KEY_ID],
    #             product.Product.KEY_PRODUCT_DATA: product_data_store_index
    #         },
    #         update={
    #             '$set': product_data_dictionary
    #         },
    #         upsert=True
    #     )

    #     # if not self.__is_product_data_set(
    #     #         product,
    #     #         product_data_dictionary,
    #     #         # subject=product1[product.Product.KEY_PRODUCT_DATA], 
    #     #         # index=product_data_store_index,
    #     #     ):
    #             # logging.info('Store data is set.')
    #             # self.products_collection.update(
    #             #     {
                        
    #             #     }, 
    #             #     {
    #             #         '$push': {
    #             #             product.Product.KEY_PRODUCT_DATA: \
    #             #                 product_data_dictionary,
    #             #         }
    #             #     }
    #             # )