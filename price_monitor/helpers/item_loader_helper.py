from scrapy import loader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from scrapy.http.response.html import HtmlResponse
from price_monitor.items import (
    global_trade_item_number_item,
    image,
    text,
)
from price_monitor.item_loaders import (
    global_trade_item_number_loader,
    image_item_loader,
    text_item_loader,
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

class ItemLoaderHelper:
    @staticmethod
    def remove_latin_space(text: str):
        return text.replace(u'\xa0', u' ')
    
    @staticmethod
    def _create_text_field(
        response: HtmlResponse, 
        value: str, 
        language: str,
        store_id: str,
        sold_by: str, 
    ) -> Dict[str, Dict[str, str]]:
        item_loader = text_item_loader.TextItemLoader(response=response)
        item_loader.add_value(text.Text.KEY_VALUE, value)
        item_loader.add_value(text.Text.KEY_LANGUAGE, language)
        item_loader.add_value(text.Text.KEY_STORE_ID, store_id)
        item_loader.add_value(text.Text.KEY_SOLD_BY, sold_by)
        
        return item_loader.load_item().get_dictionary()
    
    @staticmethod
    def _create_text_field_as_language_lookup(
        response: HtmlResponse, 
        value: str, 
        language: str,
    ) -> Dict[str, Dict[str, str]]:
        item_loader = text_item_loader.TextItemLoader(response=response)
        item_loader.add_value(text.Text.KEY_VALUE, value)
        item_loader.add_value(text.Text.KEY_LANGUAGE, language)
        
        text_value = item_loader.load_item().get(text.Text.KEY_VALUE)

        return {
            language: text_value,
        }

    @staticmethod
    def _create_gtin_field(
        response: HtmlResponse, 
        type: str, 
        value: str,
    ) -> Dict[str, str]:
        gtinItemLoader = \
            global_trade_item_number_loader.GlobalTradeItemNumberItemLoader(
                response=response
            )
        gtinItemLoader.add_value(
            field_name=global_trade_item_number_item. \
                GlobalTradeItemNumberItem.KEY_VALUE, 
            value=value
        )
        gtinItemLoader.add_value(
            field_name=global_trade_item_number_item \
                .GlobalTradeItemNumberItem \
                .KEY_GTIN_TYPE, 
            value=type
        )

        return dict(gtinItemLoader.load_item())

    @staticmethod
    def _create_image_field(
        response: HtmlResponse, 
        url: str, 
        language: str,
        store_id: Optional[str],
        sold_by: str
        # is_main: bool = False,
    ) -> Dict[str, Union[str, bool]]:
        item_loader = image_item_loader.ImageItemLoader(response=response)
        item_loader.add_value(image.Image.KEY_LANGUAGE, language)
        item_loader.add_value(image.Image.KEY_URL, url)
        # item_loader.add_value(image.Image.KEY_IS_MAIN, is_main)

        # if store_id:
        item_loader.add_value(image.Image.KEY_STORE_ID, store_id)
        item_loader.add_value(image.Image.KEY_SOLD_BY, sold_by)

        return dict(item_loader.load_item())

    @staticmethod
    def _create_image_field_as_lookup(
        response: HtmlResponse,
        urls: str,
        language: str,
        store_id: Optional[str],
        sold_by: str
        # is_main: bool = False,
    ) -> Dict[str, List]:
        return {
            language: ItemLoaderHelper._create_image_field_from_list(
                response=response,
                urls=urls,
                language=language,
                store_id=store_id,
                sold_by=sold_by,
            )
        }
        
    @staticmethod
    def _create_image_field_from_list(
        response: HtmlResponse,
        urls: str,
        language: str,
        store_id: Optional[str],
        sold_by: str
        # has_main: bool = False,
    ) -> List[Dict[str, Union[str, bool]]]:
        result = []

        for url in urls:
            result.append(ItemLoaderHelper._create_image_field(
                response=response,
                url=url,
                language=language,
                store_id=store_id,
                sold_by=sold_by,
            ))
            # has_main = False # Sets the first image to be the main one, if the argument was set.

        return result