from scrapy import (
    Field,
    Item, 
)
from scrapy.utils.project import get_project_settings

class Product(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_CREATED = 'created'
    KEY_CURRENT_OFFER = 'current_offer' # Sub dictionary.
    KEY_GTIN = 'gtin' # TODO: Multiple.
    KEY_ID = '_id'
    KEY_LANGUAGE = 'language'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_NAME = 'name'
    KEY_PRODUCT_DATA = 'product_data' # Sub dictionary.
    KEY_STORE = 'store' # Sub dictionary.
    KEY_SUPPORTED_LANGUAGES = 'supported_languages'
    KEY_TAGS = 'tags'
    KEY_UPDATED = 'updated'
    KEY_VERSION = 'version' # Not an item field.

    # TODO: Names, descriptions, main image in languages, tags, 

    # Fields.
    brand = Field()
    created = Field()
    current_offer = Field() # Sub dictionary.
    _id = Field()
    gtin = Field()
    language = Field() # TODO: Pop before upload.
    model_number = Field()
    name = Field()
    product_data = Field() # Sub dictionary.
    store = Field() # Sub dictionary.
    supported_languages = Field()
    tags = Field()
    updated = Field()
    version = Field()

    #TODO: Required fields.

    def get_dictionary(self):
        dictionary = dict(self)
        dictionary[self.KEY_VERSION] = self.get_version()
        return dictionary

    def get_version(self):
        return get_project_settings().get('PRODUCT_ITEM_VERSION')