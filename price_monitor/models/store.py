from price_monitor.items import (
    global_trade_item_number_item,
    image,
    offer,
    product,
    product_data,
    store_item,
    text,
)
from price_monitor.item_loaders import (
    global_trade_item_number_loader,
    image_item_loader,
    offer_item_loader,
    store_item_loader,
    text_item_loader,
    product_data_item_loader,
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
from scrapy.http.response.html import HtmlResponse
from typing import (
    Dict, 
    List,
    Optional,
    Union,
)

class Store:
    store_id = None
    store_name = None
    sold_by = None
    region = None
    domain = None
    language = None
    allowed_domains = []
    custom_settings = {}

    def _create_product_data_dictionary(
        self, 
        response: HtmlResponse, 
        name: str,
        sku: str, 
        brand: Optional[str] = None,
        description: Optional[str] = None,
        upc: Optional[str] = None,
        model_number: Optional[str] = None,
        images: Optional[List] = None,
        volume: Optional[str] = None,
        weight: Optional[str] = None,
        length: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
    ) -> Dict:
        item_loader = \
            product_data_item_loader.ProductDataItemLoader(response=response)

        item_loader.add_value(
            field_name=product_data.ProductData.KEY_URL,
            value=response.url,
        )
        item_loader.add_value(
            field_name=product_data.ProductData.KEY_NAME,
            value=self._create_text_field(
                response=response,
                value=name,
                language=self.language,
            ),
        )
        item_loader.add_value(
            field_name=product_data.ProductData.KEY_SKU, 
            value=sku,
        )
        item_loader.add_value(
            field_name=product_data.ProductData.KEY_SOLD_BY,
            value=self.sold_by,
        )
        item_loader.add_value(
            field_name=product_data.ProductData.KEY_STORE_ID, 
            value=self.store_id,
        )
        item_loader.add_value(
            field_name=product_data.ProductData.KEY_SUPPORTED_LANGUAGES,
            value=self._create_supported_languages_field(self.language),
        )      

        if brand:
            item_loader.add_value(
                field_name=product_data.ProductData.KEY_BRAND,
                value=brand,
            )

        # TODO: Desc.
        if description:
            item_loader.add_value(
                field_name=product_data.ProductData.KEY_DESCRIPTION,
                value=description,
            )
            pass

        if upc:
            item_loader.add_value(
                field_name=product_data.ProductData.KEY_GTIN,
                value=self._create_gtin_field(
                    response=response,
                    type=global_trade_item_number \
                        .GlobalTradeItemNumber.UPCA.value,
                    value=upc,
                ),
            )

        if model_number:
            item_loader.add_value(
                field_name=product_data.ProductData.KEY_MODEL_NUMBER,
                value=model_number,
            )

        if images:  
            item_loader.add_value(
                field_name=product_data.ProductData.KEY_IMAGES,
                value=images,
            )

        return (item_loader.load_item()).get_dictionary()

    def _create_offer_dictionary(
        self, 
        response: HtmlResponse,
        amount: str, 
        availability: str, 
        condition: str, 
        currency: str, 
        sold_by: str, 
        store_id: str
    ) -> Dict[str, str]:
        item_loader = offer_item_loader.OfferItemLoader(response=response)
        item_loader.add_value(offer.Offer.KEY_AMOUNT, str(amount))
        item_loader.add_value(
            offer.Offer.KEY_AVAILABILITY, 
            self._determine_availability(availability)
        )
        item_loader.add_value(offer.Offer.KEY_CONDITION, condition)
        item_loader.add_value(offer.Offer.KEY_CURRENCY, currency)
        item_loader.add_value(offer.Offer.KEY_SOLD_BY, sold_by)
        item_loader.add_value(offer.Offer.KEY_STORE_ID, store_id)

        return dict(item_loader.load_item())

    def _create_store_dictionary(
        self, 
        response: HtmlResponse,
        domain: str, 
        store_id: str, 
        store_name: str, 
        region: str
    ) -> Dict[str, str]:
        item_loader = store_item_loader.StoreItemLoader(response=response)
        item_loader.add_value(store_item.StoreItem.KEY_DOMAIN, domain)
        item_loader.add_value(store_item.StoreItem.KEY_ID, store_id)
        item_loader.add_value(store_item.StoreItem.KEY_NAME, store_name)
        item_loader.add_value(store_item.StoreItem.KEY_REGION, region)

        return dict(item_loader.load_item())

    def _determine_language_from_url(self, url: str) -> str:
        return language.Language.ANY.value

    def _determine_availability(self, data: Dict) -> str:
        return availability.Availability.UNKNOWN.value

    def _create_image_field(
        self, 
        response: HtmlResponse, 
        url: str, 
        language: str,
        store_id: Optional[str],
        is_main: bool = False,
    ) -> Dict[str, Union[str, bool]]:
        item_loader = image_item_loader.ImageItemLoader(response=response)
        item_loader.add_value(image.Image.KEY_LANGUAGE, language)
        item_loader.add_value(image.Image.KEY_URL, url)
        item_loader.add_value(image.Image.KEY_IS_MAIN, is_main)

        if store_id:
            item_loader.add_value(image.Image.KEY_STORE_ID, store_id)

        return dict(item_loader.load_item())

    def _create_image_field_from_list(
        self,
        response: HtmlResponse,
        urls: str,
        language: str,
        store_id: Optional[str],
        has_main: bool = False,
    ) -> List[Dict[str, Union[str, bool]]]:
        result = []

        for url in urls:
            result.append(self._create_image_field(response, url, language, store_id, has_main))
            has_main = False # Sets the first image to be the main one, if the argument was set.

        return result

    def _create_text_field(
        self, 
        response: HtmlResponse, 
        value: str, 
        language: str,
    ) -> Dict[str, Dict[str, str]]:
        item_loader = text_item_loader.TextItemLoader(response=response)
        item_loader.add_value(text.Text.KEY_LANGUAGE, language)
        item_loader.add_value(text.Text.KEY_VALUE, value)

        return {
            language: dict(item_loader.load_item())
        }

    def _create_supported_languages_field(
        self, 
        language: str
    ) -> Dict[str, Dict]:

        return {
            language: {}
        }

    def _create_gtin_field(
        self, 
        response: HtmlResponse, 
        type: str, 
        value: str
    ) -> Dict[str, str]:
        gtinItemLoader = \
            global_trade_item_number_loader.GlobalTradeItemNumberItemLoader(
                response=response
            )
        gtinItemLoader.add_value(
            global_trade_item_number_item \
                .GlobalTradeItemNumberItem \
                .KEY_GTIN_TYPE, 
            type
        )
        gtinItemLoader.add_value(
            global_trade_item_number_item.GlobalTradeItemNumberItem.KEY_VALUE, 
            value
        )

        return dict(gtinItemLoader.load_item())