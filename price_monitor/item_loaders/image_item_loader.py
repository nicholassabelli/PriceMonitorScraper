# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import image

class ImageItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, replace_entities)
    default_output_processor = TakeFirst()
    default_item_class = image.Image