# -*- coding: utf-8 -*-

from scrapy import Item, Field

class StoreItem(Item):
    # Array indexes.
    KEY_ID = '_id'
    KEY_CREATED = 'created'
    KEY_DOMAIN = 'domain'
    KEY_NAME = 'name'  
    KEY_REGION = 'region'
    KEY_UPDATED = 'updated'

    # Fields.
    _id = Field()
    created = Field()
    domain = Field()
    name = Field()
    region = Field()
    updated = Field()
    