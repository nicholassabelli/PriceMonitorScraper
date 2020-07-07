from scrapy import loader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from scrapy.http.response.html import HtmlResponse
from price_monitor.items import (
    global_trade_item_number_item,
    image,
    language_data,
    text,
)
from price_monitor.item_loaders import (
    global_trade_item_number_loader,
    image_item_loader,
    language_data_item_loader,
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
    def _create_text_field(
        response: HtmlResponse, 
        value: str, 
        language: str,
    ) -> Dict[str, Dict[str, str]]:
        item_loader = text_item_loader.TextItemLoader(response=response)
        item_loader.add_value(text.Text.KEY_VALUE, value)
        item_loader.add_value(text.Text.KEY_LANGUAGE, language)
        
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
        source: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Union[str, bool]]:
        item_loader = image_item_loader.ImageItemLoader(response=response)
        item_loader.add_value(image.Image.KEY_LANGUAGE, language)
        item_loader.add_value(image.Image.KEY_URL, url)
        
        return dict(item_loader.load_item())
        
    @staticmethod
    def _create_image_field_from_list(
        response: HtmlResponse,
        urls: str,
    ) -> List[Dict[str, Union[str, bool]]]:
        result = []

        for url in urls:
            result.append(ItemLoaderHelper._create_image_field(
                response=response,
                url=url,
            ))

        return result

    @staticmethod
    def _create_language_data_field(
        response: HtmlResponse,
        brand: str,
        images: List,
        name: str,
        url: str,
        description: Optional[str] = None,
        breadcrumbs: Optional[List] = None,
    ) -> List[str]:
        item_loader = language_data_item_loader.LanguageDataItemLoader(
            response=response
        ).add_name(name=name) \
        .add_brand(brand=brand) \
        .add_images(images=images) \
        .add_url(url=url)

        if description:
            item_loader.add_description(description=description)

        if breadcrumbs:
            item_loader.add_breadcrumbs(breadcrumbs=breadcrumbs)

        return item_loader.load_item().get_dictionary()
    