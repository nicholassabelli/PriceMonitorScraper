from __future__ import annotations
from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    Identity,
    MapCompose,
    TakeFirst
)
from w3lib.html import (
    replace_entities,
    replace_escape_chars,
    remove_tags
)
from price_monitor.items import product
from scrapy.http.response.html import HtmlResponse
from price_monitor.helpers import item_loader_helper
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

# def remove_latin_space(text): # TODO: Move.
#     return text.replace(u'\xa0', u' ')

class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(
        remove_tags, 
        replace_escape_chars, 
        item_loader_helper.ItemLoaderHelper.remove_latin_space, 
        replace_entities
    )
    default_output_processor = TakeFirst()
    default_item_class = product.Product
    brand_in = Identity()
    brand_out = Identity()
    current_offer_in = Identity()
    gtin_in = Identity()
    name_in = Identity()
    name_out = Identity()
    product_data_in = Identity()
    store_in = Identity()

    def add_brand(
        self, 
        response: HtmlResponse, 
        brand: str, #TODO: Optional?
        language: str, 
        store_id: str,
        sold_by: str,
    ) -> ProductItemLoader:
        self.add_value(
            field_name=product.Product.KEY_BRAND,
            value=[item_loader_helper.ItemLoaderHelper._create_text_field(
                response=response,
                value=brand,
                language=language,
                store_id=store_id,
                sold_by=sold_by,
            )],
        )
        return self

    def add_model_number(self, model_number: str) -> ProductItemLoader:
        self.add_value(
            field_name=product.Product.KEY_MODEL_NUMBER, 
            value=model_number #TODO: Optional?
        )
        return self

    def add_name(
        self, 
        response: HtmlResponse, 
        name: str, 
        language: str, 
        store_id: str,
        sold_by: str,
    ) -> ProductItemLoader:
        self.add_value(
            field_name=product.Product.KEY_NAME,
            value=[item_loader_helper.ItemLoaderHelper._create_text_field(
                response=response,
                value=name,
                language=language,
                store_id=store_id,
                sold_by=sold_by,
            )],
        )
        return self

    def add_offer_dictionary(
        self, 
        offer_dictionary: Dict
    ) -> ProductItemLoader:
        self.add_value(
            field_name=product.Product.KEY_CURRENT_OFFER, 
            value=offer_dictionary
        )
        return self

    def add_product_data_dictionary(
        self, 
        product_data_dictionary: Dict
    ) -> ProductItemLoader:
        self.add_value(
            field_name=product.Product.KEY_PRODUCT_DATA, 
            value=product_data_dictionary
        )
        return self

    def add_store_dictionary(
        self, 
        store_dictionary: Dict
    ) -> ProductItemLoader:
        self.add_value(
            field_name=product.Product.KEY_STORE, 
            value=store_dictionary
        )
        return self

    def add_upc(self, response: HtmlResponse, upc: str) -> ProductItemLoader: #TODO: Optional? UPC
        self.add_value(
            field_name=product.Product.KEY_GTIN,
            value=item_loader_helper.ItemLoaderHelper._create_gtin_field(
                response=response,
                type=global_trade_item_number \
                    .GlobalTradeItemNumber.UPCA.value,
                value=upc,
            ),
        )
        return self


    # TODO: Check fields are all filled and warn if not and return nothing.