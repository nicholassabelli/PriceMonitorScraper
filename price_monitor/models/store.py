from typing import Dict, Optional
from scrapy.http.response.html import HtmlResponse
from price_monitor.items import (
    global_trade_item_number_item,
    offer,
    store_item,
    text
)
from price_monitor.item_loaders import (
    global_trade_item_number_loader,
    offer_item_loader,
    store_item_loader,
    text_item_loader
)
from price_monitor.models import (
    availability,
    condition,
    curreny,
    global_trade_item_number,
    language,
    region,
    store,
    universal_product_code
)

class Store:
    def _get_offer_with_dictionary( # TODO: Rename.
        self, 
        response: HtmlResponse,
        amount: str, 
        availability: str, 
        condition: str, 
        currency: str, 
        datetime: str, 
        sold_by: str, 
        store_id: str
    ) -> Dict[str, str]:
        offerLoader = offer_item_loader.OfferItemLoader(response=response)

        offerLoader.add_value(offer.Offer.KEY_AMOUNT, str(amount))
        offerLoader.add_value(
            offer.Offer.KEY_AVAILABILITY, 
            self._get_availability_with_dictionary(availability)
        )
        offerLoader.add_value(offer.Offer.KEY_CONDITION, condition)
        offerLoader.add_value(offer.Offer.KEY_CURRENCY, currency)
        offerLoader.add_value(offer.Offer.KEY_DATETIME, datetime)
        # offerLoader.add_value(offer.Offer.KEY_SKU, sku)
        offerLoader.add_value(offer.Offer.KEY_SOLD_BY, sold_by)
        offerLoader.add_value(offer.Offer.KEY_STORE_ID, store_id)

        return dict(offerLoader.load_item())
        # sku: str, 

    def _get_store_with_dictionary(
        self, 
        response: HtmlResponse,
        domain: str, 
        store_id: str, 
        store_name: str, 
        region: str
    ) -> Dict[str, str]:
        storeLoader = store_item_loader.StoreItemLoader(response=response)
        storeLoader.add_value(store_item.StoreItem.KEY_DOMAIN, domain)
        storeLoader.add_value(store_item.StoreItem.KEY_ID, store_id)
        storeLoader.add_value(store_item.StoreItem.KEY_NAME, store_name)
        storeLoader.add_value(store_item.StoreItem.KEY_REGION, region)
        return dict(storeLoader.load_item())

    def _get_availability_with_dictionary(self, data: dict):
        return 

    def _get_text_field(
        self, 
        response: HtmlResponse, 
        value: str, 
        language: str
    ) -> Dict[str, str]:
        textItemLoader = text_item_loader.TextItemLoader(response=response)
        textItemLoader.add_value(text.Text.KEY_LANGUAGE, language)
        textItemLoader.add_value(text.Text.KEY_VALUE, value)
        return {
            language: dict(textItemLoader.load_item())
        }

    def _get_gtin_field(
        self, 
        response: HtmlResponse, 
        type: str, 
        value: str
    ) -> Dict[str, str]:
        gtinItemLoader = global_trade_item_number_loader.GlobalTradeItemNumberItemLoader(response=response)
        gtinItemLoader.add_value(global_trade_item_number_item.GlobalTradeItemNumberItem.KEY_GTIN_TYPE, type)
        gtinItemLoader.add_value(global_trade_item_number_item.GlobalTradeItemNumberItem.KEY_VALUE, value)
        return dict(gtinItemLoader.load_item())

    def _determine_language_from_url(self, url: str):
        pass