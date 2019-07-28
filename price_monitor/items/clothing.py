# -*- coding: utf-8 -*-

from scrapy import Field
from price_monitor.items.product import Product

# Clothing or accessory. 
class Clothing(Product):
    size = Field()