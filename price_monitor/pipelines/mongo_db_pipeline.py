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

        # TODO: Handle errors.
        store_seller_key = list(product_data_dictionary.keys())[0]
        lang = language.Language.EN.value # TODO: Use lang from dict.

        # Add/fix datetime fields.
        self.__add_or_fix_datetime_field(
            offer_dictionary=offer_dictionary,
            product_data_store_dictionary=product_data_dictionary[
                store_seller_key
            ],
            product_dictionary=product_dictionary,
            store_dictionary=store_dictionary,
            supported_languages_dictionary=product_data_dictionary \
                [store_seller_key] \
                [product_data.ProductData.KEY_SUPPORTED_LANGUAGES],
            lang=lang,
        )

        self.__upsert_store(store_dictionary)

        insertProduct = False       
        product_by_store_and_number = None
        product_by_gtin = self.__find_product_by_gtin(product_dictionary) \
            if product_dictionary.get(product.Product.KEY_GTIN) else None

        if not product_by_gtin:
            product_by_store_and_number = \
                self.__find_product_by_model_number_and_brand(
                    # store_seller_key=store_seller_key,
                    model_number=product_dictionary[
                        product.Product.KEY_MODEL_NUMBER
                    ],
                    brand=product_dictionary[
                        product.Product.KEY_BRAND
                    ],
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

            if not self.__is_product_data_set(
                subject=product1[product.Product.KEY_PRODUCT_DATA], 
                index=store_seller_key,
            ):
                logging.info('Store data is set.')

                product_data_store_seller_index = \
                    self.__create_product_data_dictionary_store_seller_index(
                        store_seller_key=store_seller_key,
                    )

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
                        },
                    },
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
        # offer_dictionary[offer.Offer.KEY_DATETIME] = datetime.fromisoformat(
        #     offer_dictionary['datetime']
        # )

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
        store_seller_key
    ):
        return product.Product.KEY_PRODUCT_DATA \
                    + '.' + store_seller_key

    def __find_product_by_gtin(self, product_dictionary):
        return self.products_collection.find_one({
            product.Product.KEY_GTIN: product_dictionary[
                product.Product.KEY_GTIN
            ]
        })
    
    def __find_product_by_model_number_and_brand(
        self, 
        # store_seller_key,
        model_number, 
        brand,
    ):
        # product_data_store_seller_index = \
        #     self.__create_product_data_dictionary_store_seller_index(
        #     store_seller_key
        # )
        brand_regex = re.compile(f'^{brand}$', re.IGNORECASE)
        
        return self.products_collection.find_one(
            {
                '$and': [
                    # {
                    #     product_data_store_seller_index: { '$exists': True }
                    # },
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
        lang
    ):
        dictionaries = [
            offer_dictionary,
            product_data_store_dictionary,
            product_dictionary,
            store_dictionary,
        ]

        # TODO: Add index to item to avoid this loop.
        # Add the supported lang dict to the array of dicts to fix.
        # for lang in language.Language:
        x = supported_languages_dictionary.get(lang)

        if x is not None:
            dictionaries.append(supported_languages_dictionary[
                lang
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
                '$setOnInsert': store_dictionary,
            },
            upsert=True,
        )
        # logging.log(logging.INFO, "Added store to database!")