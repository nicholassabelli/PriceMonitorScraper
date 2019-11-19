# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Text(Item):
    # Array indexes. 
    KEY_LANGUAGE = 'language'
    KEY_VALUE = 'value'

    # Fields.
    language = Field()
    value = Field()

    # def __init__(self, language, value):
    #     self.language = language
    #     self.value = value

    def get_dictionary(self):
        return dict(self)