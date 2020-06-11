# -*- coding: utf-8 -*-

from scrapy import Item, Field

class ProductData(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_COLOUR = 'colour'
    KEY_CREATED = 'created'
    KEY_DESCRIPTION = 'description'
    KEY_GTIN = 'gtin'
    KEY_HEIGHT = 'height'
    KEY_IMAGES = 'images'
    KEY_LENGTH = 'length'
    # KEY_MEASUREMENTS = 'measurements'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_NAME = 'name'
    KEY_RELEASE_DATE = 'release_date'
    KEY_SKU = 'sku'
    KEY_SOLD_BY = 'sold_by'
    KEY_STORE_ID = 'store_id'
    KEY_SUPPORTED_LANGUAGES = 'supported_languages'
    KEY_TAGS = 'tags'
    KEY_UPDATED = 'updated'
    KEY_URL = 'url'
    KEY_WEIGHT_OR_VOLUME = 'weight_or_volume'

    KEY_WIDTH = 'width'
    # TODO: Schema version.
    # KEY_SCHEMA_VERSION = 'schema_version'

    # TODO: 
    KEY_WEIGHT = 'weight'
    KEY_VOLUME = 'volume'
    # or
    KEY_SIZE = ''

    # Fields.
    brand = Field()
    colour = Field()
    created = Field()
    description = Field()
    gtin = Field()
    # height = Field()
    images = Field()
    # length = Field()
    # lookup = Field()
    model_number = Field()
    name = Field()
    release_date = Field()
    sku = Field()
    sold_by = Field()
    store_id = Field()
    supported_languages = Field()
    tags = Field()
    updated = Field()
    url = Field()
    weight_or_volume = Field()
    # width = Field()

    def get_dictionary(self):
        value_dict = dict(self)

        return {
            self.__create_product_data_dictionary_store_index(
                value_dict[self.KEY_STORE_ID], value_dict[self.KEY_SOLD_BY]
            ): value_dict
        }

    def __create_product_data_dictionary_store_index(self, store_id, sold_by): #TODO: Put in a model.
        return f"{store_id} ({sold_by})".replace(".", "")