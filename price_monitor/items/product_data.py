from scrapy import (
    Field,
    Item,
)

class ProductData(Item):
    # Array indexes.
    # KEY_BRAND = 'brand'
    # KEY_BREADCRUMBS = 'breadcrumbs'
    KEY_COLOUR = 'colour'
    KEY_CREATED = 'created'
    KEY_DESCRIPTION = 'description'
    # KEY_DOMAIN = ''
    KEY_GTIN = 'gtin'
    KEY_HEIGHT = 'height'
    KEY_IMAGES = 'images'
    KEY_LANGUAGE_DATA = 'language_data'
    KEY_LENGTH = 'length'
    # KEY_MEASUREMENTS = 'measurements'
    KEY_MODEL_NUMBER = 'model_number'
    KEY_NAME = 'name'
    KEY_RELEASE_DATE = 'release_date'
    KEY_SKU = 'sku'
    KEY_SOURCE = 'source'
    KEY_SOLD_BY = 'sold_by'
    KEY_STORE_ID = 'store_id'
    # KEY_SUPPORTED_LANGUAGES = 'supported_languages'
    KEY_TAGS = 'tags'
    KEY_UPDATED = 'updated'
    KEY_URL = 'url'
    KEY_WEIGHT_OR_VOLUME = 'weight_or_volume'

    KEY_WIDTH = 'width'
    # TODO: Schema version.
    KEY_VERSION = 'version'

    # TODO: 
    KEY_WEIGHT = 'weight'
    KEY_VOLUME = 'volume'
    # or
    KEY_SIZE = ''

    # Fields.
    brand = Field()
    # breadcrumbs = Field()
    colour = Field()
    created = Field()
    description = Field()
    # domain = Field()
    gtin = Field()
    # height = Field()
    images = Field()
    # length = Field()
    # lookup = Field()
    language_data = Field()
    model_number = Field()
    name = Field()
    release_date = Field()
    sku = Field()
    source = Field()
    sold_by = Field()
    store_id = Field()
    # supported_languages = Field()
    tags = Field()
    updated = Field()
    url = Field()
    weight_or_volume = Field()
    # width = Field()

    version = Field()

    def get_dictionary(self):
        value_dict = dict(self)

        return {
            self.__create_product_data_dictionary_store_index(
                value_dict[self.KEY_STORE_ID], value_dict[self.KEY_SOLD_BY]
            ): value_dict
        }

    def __create_product_data_dictionary_store_index(self, store_id, sold_by): #TODO: Put in a model.
        return f"{store_id} ({sold_by})".replace(".", "")