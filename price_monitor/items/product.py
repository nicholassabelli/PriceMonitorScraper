# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Product(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_CREATED = 'created'
    KEY_CURRENT_OFFER = 'current_offer' # Sub dictionary.
    KEY_ID = '_id'
    KEY_LANGUAGE = 'language'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_NAME = 'name'
    KEY_PRODUCT_DATA = 'product_data' # Sub dictionary.
    KEY_STORE = 'store' # Sub dictionary.
    KEY_GTIN = 'gtin' # TODO: Multiple.
    KEY_UPDATED = 'updated'

    # TODO: Names, descriptions, main image in languages, tags, 

    # Fields.
    brand = Field()
    created = Field()
    current_offer = Field() # Sub dictionary.
    _id = Field()
    language = Field() # TODO: Pop before upload.
    model_number = Field()
    name = Field()
    product_data = Field() # Sub dictionary.
    store = Field() # Sub dictionary.
    gtin = Field()
    updated = Field()

    def get_dictionary(self):
        return dict(self)