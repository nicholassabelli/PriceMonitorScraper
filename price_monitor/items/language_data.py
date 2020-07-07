from scrapy import (
    Field,
    Item,
)

class LanguageData(Item):
    # Array indexes.
    KEY_BRAND = 'brand'
    KEY_BREADCRUMBS = 'breadcrumbs'
    KEY_COLOUR = 'colour'
    KEY_CREATED = 'created'
    KEY_DESCRIPTION = 'description'
    KEY_IMAGES = 'images'
    KEY_NAME = 'name'
    KEY_TAGS = 'tags'
    KEY_UPDATED = 'updated'
    KEY_URL = 'url'

    # Fields.
    brand = Field()
    breadcrumbs = Field()
    colour = Field()
    created = Field()
    description = Field()
    images = Field()
    name = Field()
    tags = Field()
    updated = Field()
    url = Field()

    def get_dictionary(self):
        return dict(self)