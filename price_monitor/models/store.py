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
    version = None
    allowed_domains = []
    custom_settings = {}

    def _create_product_dictionary(
        self, 
        response: HtmlResponse, 
        data: Optional[Dict] = None,
    ) -> product.Product:
        pass

    def _create_product_data_dictionary(
        self, 
        response: HtmlResponse,
        name: str, 
        brand: Optional[str] = None,
        model_number: Optional[str] = None,
        upc: Optional[str] = None,
        data: Optional[Dict] = None,
    ) -> Dict:
        pass

    def _create_offer_dictionary(
        self, 
        response: HtmlResponse, 
        data: Optional[Dict] = None,
    ) -> Dict:
        pass

    def _create_store_dictionary(self, response: HtmlResponse) -> Dict:
        item = store_item_loader.StoreItemLoader(response=response) \
            .add_id(id=self.store_id) \
            .add_name(name=self.store_name) \
            .add_domain(domain=self.domain) \
            .add_region(region=self.region) \
            .load_item()

        return item.get_dictionary()

    def _determine_language_from_url(self, url: str) -> str:
        return language.Language.ANY.value

    def _determine_availability(self, data: Dict) -> str:
        return availability.Availability.UNKNOWN.value