from __future__ import annotations
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import store_item

class StoreItemLoader(ItemLoader):
    default_input_processor = MapCompose(
        remove_tags, 
        replace_escape_chars, 
        replace_entities
    )
    default_output_processor = TakeFirst()
    default_item_class = store_item.StoreItem

    def add_domain(self, domain: str) -> StoreItemLoader: # TODO: Can have multiple domains, ex: staples, 
        self.add_value(
            field_name=store_item.StoreItem.KEY_DOMAIN,
            value=domain,
        )
        return self

    def add_id(self, id: str) -> StoreItemLoader:
        self.add_value(
            field_name=store_item.StoreItem.KEY_ID,
            value=id,
        )
        return self
    
    def add_name(self, name: str) -> StoreItemLoader:
        self.add_value(
            field_name=store_item.StoreItem.KEY_NAME, 
            value=name,
        )
        return self

    def add_region(self, region: str) -> StoreItemLoader:
        self.add_value(
            field_name=store_item.StoreItem.KEY_REGION, 
            value=region,
        )
        return self