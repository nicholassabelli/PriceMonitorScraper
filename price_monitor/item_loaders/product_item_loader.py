# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import product

def remove_latin_space(text): # TODO: Move.
    return text.replace(u'\xa0', u' ')

class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, remove_latin_space, replace_entities)
    default_output_processor = TakeFirst()
    default_item_class = product.Product
    current_offer_in = Identity()
    store_in = Identity()
    product_data_in = Identity()
    gtin_in = Identity()

