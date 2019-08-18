# -*- coding: utf-8 -*-

from scrapy import Item, Field

class ProductData(Item):
    # Array indexes.
    KEY_LOOKUP = 'lookup'
    KEY_VALUES = 'values'
    
    # Fields.
    lookup = Field()
    values = Field()

    def get_dictionary(self):
        return dict(self)