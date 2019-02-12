# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class PriceCheckerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class Price(Item):
    amount = Field()
    currency = Field()

class Product(Item):
    name = Field()
    description = Field()
    currentPrice = Field(input_processor=Identity()) # handle quebec prices
    url = Field()
    releaseDate = Field()
    availability = Field()
    upc = Field()
    tags = Field()
    # soldby
    # images

class PriceItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()
    default_item_class = Price

class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()       # move to property to allow again
    default_item_class = Product