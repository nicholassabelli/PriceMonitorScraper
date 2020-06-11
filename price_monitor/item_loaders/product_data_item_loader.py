from __future__ import annotations
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import product_data
from price_monitor.item_loaders import product_item_loader
from scrapy.http.response.html import HtmlResponse
from price_monitor.helpers import item_loader_helper
from price_monitor.items import (
    global_trade_item_number_item,
    image,
    offer,
    product,
    product_data,
    store_item,
    text,
)
from price_monitor.models import (
    availability,
    condition,
    curreny,
    global_trade_item_number,
    language,
    region,
    store,
    universal_product_code,
)
from typing import (
    Dict, 
    List,
    Optional,
    Union,
)

class ProductDataItemLoader(ItemLoader):
    default_input_processor = MapCompose(
        remove_tags, 
        replace_escape_chars, 
        item_loader_helper.ItemLoaderHelper.remove_latin_space, 
        replace_entities,
    )
    default_output_processor = TakeFirst()
    default_item_class = product_data.ProductData
    brand_in = Identity()
    description_in = Identity()
    gtin_in = Identity()
    images_in = Identity()
    # images_out = Identity()
    name_in = Identity()
    supported_languages_in = Identity()

    def add_brand(
        self, 
        response: HtmlResponse, 
        brand: str, 
        language: str
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_BRAND,
            value=item_loader_helper.ItemLoaderHelper \
                ._create_text_field_as_language_lookup(
                    response=response,
                    value=brand,
                    language=language,
            ),
        )
        return self

    def add_description(
        self, 
        response: HtmlResponse, 
        description: str, 
        language: str
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_DESCRIPTION,
            value=item_loader_helper.ItemLoaderHelper \
                ._create_text_field_as_language_lookup(
                    response=response,
                    value=description,
                    language=language,
            ),
        )
        return self

    def add_images(
        self,
        response: HtmlResponse,
        urls: List,
        language: str,
        store_id: str,
        sold_by: str,
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_IMAGES,
            value=item_loader_helper.ItemLoaderHelper \
                ._create_image_field_from_list(
                    response=response,
                    urls=urls,
                    language=language,
                    store_id=store_id,
                    sold_by=sold_by,
            ),
        )
        return self

    def add_images_as_lookup(
        self,
        response: HtmlResponse,
        urls: List,
        language: str,
        store_id: str,
        sold_by: str,
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_IMAGES,
            value=item_loader_helper.ItemLoaderHelper \
                ._create_image_field_as_lookup(
                    response=response,
                    urls=urls,
                    language=language,
                    store_id=store_id,
                    sold_by=sold_by,
            ),
        )
        return self

    def add_model_number(self, model_number: str) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_MODEL_NUMBER,
            value=model_number,
        )
        return self

    def add_name(
        self, 
        response: HtmlResponse, 
        name: str, 
        language: str
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_NAME,
            value=item_loader_helper.ItemLoaderHelper \
                ._create_text_field_as_language_lookup(
                    response=response,
                    value=name,
                    language=language,
            ),
        )
        return self

    def add_sku(self, sku: str) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_SKU, 
            value=sku,
        )
        return self    

    def add_sold_by(self, sold_by: str) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_SOLD_BY,
            value=sold_by,
        )
        return self
    
    def add_store_id(self, store_id: str) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_STORE_ID, 
            value=store_id,
        )
        return self

    def add_supported_language(self, language: str) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_SUPPORTED_LANGUAGES,
            value=self.__create_supported_languages_field(language),
        )
        return self

    def add_upc(
        self, 
        response: HtmlResponse, 
        upc: str
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_GTIN,
            value=item_loader_helper.ItemLoaderHelper._create_gtin_field(
                response=response,
                type=global_trade_item_number \
                    .GlobalTradeItemNumber.UPCA.value,
                value=upc,
            ),
        )
        return self

    def add_url(self, url: str) -> ProductDataItemLoader: # TODO: Can be different in different languages.
        self.add_value(
            field_name=product_data.ProductData.KEY_URL,
            value=url,
        )
        return self

    def __create_supported_languages_field(
        self, 
        language: str,
    ) -> Dict[str, Dict]:
        return {
            language: {}
        }