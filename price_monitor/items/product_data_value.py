# -*- coding: utf-8 -*-

from scrapy import Item, Field

class ProductDataValue(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_COLOUR = 'colour'
    KEY_CREATED = 'created'
    KEY_DESCRIPTION = 'description'
    KEY_HEIGHT = 'height'
    KEY_IMAGES = 'images'
    KEY_LENGTH = 'length'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_NAME = 'name'
    KEY_RELEASE_DATE = 'release_date'
    KEY_SKU = 'sku'
    KEY_SOLD_BY = 'sold_by'
    KEY_STORE_ID = 'store_id'
    KEY_TAGS = 'tags'
    KEY_UPC = 'upc'
    KEY_UPDATED = 'updated'
    KEY_URL = 'url'
    KEY_WEIGHT_OR_VOLUME = 'weight_or_volume'
    KEY_WIDTH = 'width'
    
    # Fields.
    brand = Field()
    colour = Field()
    created = Field()
    description = Field()
    height = Field()
    images = Field()
    length = Field()
    lookup = Field()
    model_number = Field()
    name = Field()
    release_date = Field()
    sku = Field()
    sold_by = Field()
    store_id = Field()
    tags = Field()
    upc = Field()
    updated = Field()
    url = Field()
    weight_or_volume = Field()
    width = Field()

    def get_dictionary(self):
        return dict(self)