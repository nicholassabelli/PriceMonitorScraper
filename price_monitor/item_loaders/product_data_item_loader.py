from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import product_data
from price_monitor.item_loaders import product_item_loader

class ProductDataItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, product_item_loader.remove_latin_space, replace_entities)
    default_output_processor = TakeFirst()
    default_item_class = product_data.ProductData
    name_in = Identity()
    # name_out = Identity()
    description_in = Identity()
    # description_out = Identity()
    gtin_in = Identity()
    supported_languages_in = Identity()

