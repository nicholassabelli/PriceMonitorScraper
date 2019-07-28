# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Product(Item):
    # Array indexes.
    KEY_NAME = 'name'
    KEY_DESCRIPTION = 'description'
    KEY_CURRENT_PRICE = 'current_price'
    KEY_URL = 'url'
    KEY_RELEASE_DATE = 'release_date'
    KEY_AVAILABILITY = 'availability'
    KEY_UPC = 'upc'
    KEY_TAGS = 'tags'
    KEY_BRAND = 'brand'
    KEY_LENGTH = 'length'
    KEY_WIDTH = 'width'
    KEY_HEIGHT = 'height'
    KEY_WEIGHT_OR_VOLUME = 'weight_or_volume'
    KEY_SIZE = 'size'
    KEY_STORE = 'store'
    KEY_SOLD_BY = 'sold_by'
    KEY_DOMAIN = 'domain'
    KEY_CREATED = 'created'
    KEY_UPDATED = 'updated'

    # Fields.
    name = Field()
    description = Field()
    current_price = Field()
    url = Field()
    release_date = Field()
    availability = Field()
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
    store = Field()
    domain = Field()
    created = Field()
    updated = Field()

    # manufacturer
    # sku
    # locale
    # region
    # model_number
    