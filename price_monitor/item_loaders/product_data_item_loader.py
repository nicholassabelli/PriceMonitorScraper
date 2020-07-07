from __future__ import annotations
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from scrapy.http.response.html import HtmlResponse
from price_monitor.helpers import (
    item_loader_helper,
    input_processor_helper,
)
from price_monitor.items import (
    product_data,
)
from price_monitor.models import (
    global_trade_item_number,
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
        input_processor_helper.InputProcessorHelper.remove_latin_space, 
        replace_entities,
    )
    default_output_processor = TakeFirst()
    default_item_class = product_data.ProductData
    gtin_in = Identity()
    language_data_in = Identity()

    def add_language_data(
        self,
        response: HtmlResponse,
        brand: str,
        images: List,
        name: str,
        url: str,
        description: Optional[str] = None,
        breadcrumbs: Optional[List] = None,
    ) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_LANGUAGE_DATA,
            value=item_loader_helper.ItemLoaderHelper._create_language_data_field(
                response=response,
                brand=brand,
                images=images,
                name=name,
                url=url,
                description=description,
                breadcrumbs=breadcrumbs,
            ),
        )
        return self

    def add_model_number(self, model_number: str) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_MODEL_NUMBER,
            value=model_number,
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

    def add_version(self, version: int) -> ProductDataItemLoader:
        self.add_value(
            field_name=product_data.ProductData.KEY_VERSION, 
            value=str(version)
        )
        return self