# -*- coding: utf-8 -*-

from scrapy import Field
from price_monitor.items.product import Product

class VideoGame(Product):
    # Fields.
    developers = Field()
    publishers = Field()
    platforms = Field()
    genres = Field()
    modes = Field()