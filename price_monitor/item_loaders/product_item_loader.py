# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import Product

def remove_latin_space(text):
    return text.replace(u'\xa0', u' ')

class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, remove_latin_space, replace_entities)
    default_output_processor = TakeFirst()
    default_item_class = Product
    current_price_in = Identity()
    store_in = Identity()

