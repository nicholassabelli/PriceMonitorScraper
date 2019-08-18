# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Product(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_CREATED = 'created'
    KEY_CURRENT_OFFER = 'current_offer'
    KEY_ID = '_id'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_PRODUCT_DATA = 'product_data'
    # KEY_PRODUCT_DATA_RAW = 'product_data_raw'
    # KEY_PRODUCT_DATA_LOOKUP = 'product_data_lookup'
    KEY_STORE = 'store'
    KEY_UPC = 'upc'
    KEY_UPDATED = 'updated'

    # Fields.
    brand = Field()
    created = Field()
    current_offer = Field() # Sub dictionaries.
    _id = Field()
    model_number = Field()
    product_data = Field() # Sub dictionary.
    store = Field() # Sub dictionaries.
    upc = Field()
    updated = Field()

    def get_dictionary(self):
        return dict(self)