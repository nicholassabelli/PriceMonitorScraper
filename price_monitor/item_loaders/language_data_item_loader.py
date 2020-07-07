from __future__ import annotations
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import language_data
from price_monitor.item_loaders import product_item_loader
from scrapy.http.response.html import HtmlResponse
from price_monitor.helpers import input_processor_helper
from typing import (
    Dict, 
    List,
    Optional,
    Union,
)

class LanguageDataItemLoader(ItemLoader):
    default_input_processor = MapCompose(
        remove_tags, 
        replace_escape_chars, 
        input_processor_helper.InputProcessorHelper.remove_latin_space,
        replace_entities,
    )
    default_output_processor = TakeFirst()
    default_item_class = language_data.LanguageData
    images_out = Identity()
    breadcrumbs_out = Identity()

    def add_brand(
        self, 
        brand: str, 
    ) -> LanguageDataItemLoader:
        self.add_value(
            field_name=language_data.LanguageData.KEY_BRAND,
            value=brand,
        )
        return self

    def add_breadcrumbs(
        self, 
        breadcrumbs: List, 
    ) -> LanguageDataItemLoader:
        self.add_value(
            field_name=language_data.LanguageData.KEY_BREADCRUMBS,
            value=breadcrumbs,
        )
        return self

    def add_description(
        self, 
        description: str, 
    ) -> LanguageDataItemLoader:
        self.add_value(
            field_name=language_data.LanguageData.KEY_DESCRIPTION,
            value=description,
        )
        return self

    def add_images(
        self,
        images: List,
    ) -> LanguageDataItemLoader:
        self.add_value(
            field_name=language_data.LanguageData.KEY_IMAGES,
            value=images,
        )
        return self

    def add_name(
        self, 
        name: str, 
    ) -> LanguageDataItemLoader:
        self.add_value(
            field_name=language_data.LanguageData.KEY_NAME,
            value=name,
        )
        return self

    def add_url(self, url: str) -> LanguageDataItemLoader: # TODO: Can be different in different languages.
        self.add_value(
            field_name=language_data.LanguageData.KEY_URL,
            value=url,
        )
        return self