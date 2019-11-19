# -*- coding: utf-8 -*-

from scrapy import Item, Field

class GlobalTradeItemNumberItem(Item):
    KEY_GTIN_TYPE = 'gtin_type'
    KEY_VALUE = 'value'

    gtin_type = Field()
    value = Field()

    def get_dictionary(self):
        return dict(self)