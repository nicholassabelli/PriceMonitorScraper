# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Product(Item):
    # Array indexes.
    KEY_ID = '_id'
    KEY_NAME = 'name'
    KEY_DESCRIPTION = 'description'
    KEY_CURRENT_PRICE = 'current_price' 
    KEY_URL = 'url'
    KEY_RELEASE_DATE = 'release_date'
    KEY_UPC = 'upc'
    KEY_TAGS = 'tags'
    KEY_BRAND = 'brand'
    KEY_LENGTH = 'length'
    KEY_WIDTH = 'width'
    KEY_HEIGHT = 'height'
    KEY_WEIGHT_OR_VOLUME = 'weight_or_volume'
    KEY_SIZE = 'size'
    KEY_STORE = 'store' # sub document
    KEY_SOLD_BY = 'sold_by'
    KEY_CREATED = 'created'
    KEY_UPDATED = 'updated'
    KEY_SKU = 'sku'
    KEY_MODEL_NUMBER = 'model_number'

    KEY_STORE_ID = 'store_id'

    # KEY_REGION = 'region'

    # Fields.
    name = Field()
    description = Field()
    current_price = Field() # sub document
    url = Field()
    release_date = Field()
    upc = Field()
    tags = Field()
    brand = Field()
    length = Field()
    width = Field()
    height = Field()
    weight_or_volume = Field()
    # size = Field()
    # images = Field()
    colour = Field()
    sold_by = Field()
    store = Field() # sub document
    created = Field()
    updated = Field()
    sku = Field()
    model_number = Field()


    # TODO: Fix.
    product = Field()
    store_id = Field()

    # sku
    # locale
    # region
    # model_number
    