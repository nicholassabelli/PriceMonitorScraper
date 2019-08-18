# -*- coding: utf-8 -*-

from scrapy import Item, Field

class ProductDataLookup(Item):
    # Array indexes.
    KEY_LANGUAGE = 'language'
    KEY_STORE_ID = 'store_id'
    KEY_UPDATED = 'updated'

    # Fields.
    language = Field()
    store_id = Field()
    updated = Field()

    def get_dictionary(self):
        dictionary = dict()

        dictionary[self[self.KEY_STORE_ID]] = {
            self[self.KEY_LANGUAGE]: self[self.KEY_UPDATED]
        }

        return dictionary
    