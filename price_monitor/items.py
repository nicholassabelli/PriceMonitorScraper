# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst
from w3lib.html import replace_escape_chars, remove_tags

class PriceCheckerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class Price(Item):
    # Array indexes.
    KEY_AMOUNT = 'amount'
    KEY_CURRENCY = 'currency'

    # Fields.
    amount = Field()
    currency = Field()

class Product(Item):
    # Array indexes.
    KEY_NAME = 'name'
    KEY_DESCRIPTION = 'description'
    KEY_CURRENT_PRICE = 'current_price'
    KEY_URL = 'url'
    KEY_RELEASE_DATE = 'release_date'
    KEY_AVAILABILITY = 'availability' # Enum?
    KEY_UPC = 'upc'
    KEY_TAGS = 'tags'
    KEY_BRAND = 'brand'
    KEY_LENGTH = 'length'
    KEY_WIDTH = 'width'
    KEY_HEIGHT = 'height'
    KEY_WEIGHT_OR_VOLUME = 'weight_or_volume'
    KEY_SIZE = 'size'

    # Fields.
    name = Field()
    description = Field()
    current_price = Field()
    url = Field()
    release_date = Field()
    availability = Field()
    upc = Field()
    tags = Field()
    brand = Field()
    length = Field()
    width = Field()
    height = Field()
    weight_or_volume = Field()
    # size = Field()
    # store and sold by are different 
    # images
    colour = Field()
    sold_by = Field()

class Food(Product):
    pass

# Clothing or accessory. 
class Clothing():
    size = Field()

class VideoGame(Product):
    # Fields.
    developers = Field()
    publishers = Field()
    platforms = Field()
    genres = Field()
    modes = Field()

def filter_price(value):
    if value.isdigit():
        return value

class PriceItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()
    default_item_class = Price

class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars)
    default_output_processor = TakeFirst()
    default_item_class = Product
    current_price_in = Identity()

class IGAProductItemLoader(ProductItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, lambda x: ' '.join(x.split()))

class MetroProductItemLoader(ProductItemLoader):
    tags_out = Identity()