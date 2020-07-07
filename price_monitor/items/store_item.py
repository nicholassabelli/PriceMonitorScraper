from scrapy import (
    Field,
    Item,
)
from scrapy.utils.project import get_project_settings

class StoreItem(Item):
    # Array indexes.
    KEY_ID = '_id'
    KEY_CREATED = 'created'
    KEY_DOMAIN = 'domain'
    KEY_NAME = 'name'  
    KEY_REGION = 'region'
    KEY_UPDATED = 'updated'
    KEY_VERSION = 'version' # Not an item field.

    # Fields.
    _id = Field()
    created = Field()
    domain = Field()
    name = Field()
    region = Field() # TODO: Sub-regions.
    updated = Field()

    # TODO: Locations.

    def get_dictionary(self):
        dictionary = dict(self)
        dictionary[self.KEY_VERSION] = self.get_version()
        return dictionary

    def get_version(self):
        return get_project_settings().get('STORE_ITEM_VERSION')
    