# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags, strip_html5_whitespace
from price_monitor.items import text

class TextItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, replace_entities, strip_html5_whitespace)
    default_output_processor = TakeFirst()
    default_item_class = text.Text