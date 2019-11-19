# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Product(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_CREATED = 'created'
    KEY_CURRENT_OFFER = 'current_offer'
    KEY_ID = '_id'
    KEY_LANGUAGE = 'language'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_PRODUCT_DATA = 'product_data'
    # KEY_PRODUCT_DATA_RAW = 'product_data_raw'
    # KEY_PRODUCT_DATA_LOOKUP = 'product_data_lookup'
    KEY_STORE = 'store'
    KEY_GTIN = 'gtin' # TODO: Multiple.
    KEY_UPDATED = 'updated'

    # Fields.
    brand = Field()
    created = Field()
    current_offer = Field() # Sub dictionaries.
    _id = Field()
    language = Field() # TODO: Pop before upload.
    model_number = Field()
    product_data = Field() # Sub dictionary.
    store = Field() # Sub dictionaries.
    gtin = Field()
    updated = Field()

    def get_dictionary(self):
        return dict(self)