# -*- coding: utf-8 -*-

from scrapy import Item, Field

class ProductDataSupportedLanguages(Item):
    KEY_CREATED = 'created'
    KEY_LANGUAGE = 'language'
    KEY_UPDATED = 'updated'

    created = Field()
    language = Field()
    updated = Field()

    def get_dictionary(self):
        dictionary = dict(self)
        language = dictionary.pop(self.KEY_LANGUAGE)

        return {
            language: dictionary
        }