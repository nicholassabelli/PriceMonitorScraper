# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Text(Item):
    # Array indexes. 
    KEY_LANGUAGE = 'language'
    KEY_SOLD_BY = 'sold_by'
    KEY_STORE_ID = 'store_id'
    KEY_VALUE = 'value'

    # Fields.
    language = Field()
    sold_by = Field()
    store_id = Field()
    value = Field()

    # def __init__(self, language, value):
    #     self.language = language
    #     self.value = value

    def get_dictionary(self):
        return dict(self)