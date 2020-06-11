import ast
import datetime
import logging
import json
import time
import re
from collections import namedtuple
from scrapy.http.response.html import HtmlResponse
from typing import (
    Dict, 
    List,
    Optional,
    Union,
)
from price_monitor.items import (
    offer,
    product,
    product_data,
)
from price_monitor.item_loaders import (
    offer_item_loader,
    iga_product_item_loader,
    store_item_loader,
    product_item_loader,
    product_data_item_loader,
)
from price_monitor.models import (
    availability,
    condition,
    curreny,
    global_trade_item_number,
    language,
    offer,
    region,
    store,
    universal_product_code,
)

class Metro(store.Store):
    store_id = 'metro'
    store_name = 'Metro'
    sold_by = 'Metro Inc.' #'Metro Richelieu Inc.'
    region = region.Region.CANADA.value
    domain = 'metro.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'price_monitor.pipelines.StripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            # 'price_monitor.pipelines.UniversalProductCodePipeline': 900,
            'price_monitor.pipelines.mongo_db_pipeline.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 999
        }
    }

    def parse_product(
        self, 
        response: HtmlResponse,
    ) -> Optional[product.Product]:
        self.language = self._determine_language_from_url(response.url)

        if not self.language:
            logging.error('Unable to determine language!')
            return None

        return self._create_product_dictionary(response)

    def _determine_language_from_url(self, url: str) -> str: # TODO: Replace by getting language from html tag.
        if re.search(f'www.{self.domain}/en/online-grocery/', url):
            return language.Language.EN.value
        elif re.search(f'www.{self.domain}/epicerie-en-ligne/', url):
            return language.Language.FR.value
        
        return None

    def _determine_availability(self, data: Dict) -> str:
        return availability.Availability.IN_STOCK.value if data \
            else availability.Availability.OUT_OF_STOCK.value

    # def _find_json_data(self, response: HtmlResponse) -> Optional[Dict]:
    #     css_path = "div.product-details.js-ga-productdetails > " + \
    #        "div.relative::attr(data-product)"

    #     product_data = response.css(css_path).extract()

    #     if not product_data:
    #         logging.error('Unable to load JSON data.') # TODO: Log URL.
    #         return None

    #     try:
    #         return json.loads(product_data[0])
    #     except:
    #         pass

    #     # try:
    #     #     return ast.literal_eval(product_data[0])
    #     # except:
    #     #     pass

    #     try:
    #         data = product_data[0].replace("'", '"')
    #         return json.loads(data)
    #     except:
    #         logging.error('Unable to load JSON data.')

    def _create_product_dictionary(
        self, 
        response: HtmlResponse, 
        data: Optional[Dict] = None,
    ) -> product.Product:
        try:
            upc = (
                universal_product_code.UniversalProductCode(
                    upc=response.css('span[itemprop="sku"]::text').get()
                )
            ).value
        except Exception as exception:
            logging.exception(msg='Unable to get UPC.', exc_info=exception)
            return None

        name1 = response.css(
            "div.product-info.item-addToCart > a.invisible-text::text"
        ).extract()
        name2 = response.css('title::text') \
            .extract()[0].split('|')[0]
        name = name1 or name2

        if not name:
            pass # TODO: Log error and return none.

        brand = response.css('span[itemprop="brand"]::text').extract()
        item_loader = product_item_loader.ProductItemLoader(
            response=response
        ).add_name(
            response=response,
            name=name, # TODO: What about if it's none.
            language=self.language,
            store_id=self.store_id,
            sold_by=self.sold_by,
        ).add_brand(
            response=response,
            brand=brand, # TODO: What about if it's none.
            language=self.language,
            store_id=self.store_id,
            sold_by=self.sold_by,
        ).add_upc(response=response, upc=upc) \
        .add_product_data_dictionary(
            product_data_dictionary=self._create_product_data_dictionary(
                response=response,
                data=data,
                name=name,
                brand=brand,
                upc=upc,
            ),
        ).add_offer_dictionary(
            offer_dictionary=self._create_offer_dictionary(
                response=response, 
                data=data, 
            ),
        ).add_store_dictionary(
            store_dictionary=self._create_store_dictionary(
                response=response, 
            ),
        )

        return item_loader.load_item()

    def _create_product_data_dictionary(
        self, 
        response: HtmlResponse, 
        name: str, 
        brand: Optional[str] = None,
        model_number: Optional[str] = None,
        upc: Optional[str] = None,
        data: Optional[Dict] = None,
    ) -> Dict:
        item = product_data_item_loader \
            .ProductDataItemLoader(response=response) \
            .add_name(
                response=response,
                name=name,
                language=self.language,
            ).add_brand(
                response=response,
                brand=brand,
                language=self.language,
            ).add_sku(sku=upc) \
            .add_upc(response=response, upc=upc) \
            .add_description(
                response=response,
                description=response.css(
                    'span[itemprop="description"]::text'
                ).get(),
                language=self.language,
            ).add_images_as_lookup(
                response=response,
                urls=response.css(
                    'div[itemtype="http://schema.org/Product"] \
                        > span[itemprop="image"]::text'
                ).getall(),
                language=self.language,
                store_id=self.store_id,
                sold_by=self.sold_by,
            ).add_supported_language(language=self.language) \
            .add_store_id(store_id=self.store_id) \
            .add_sold_by(sold_by=self.sold_by) \
            .load_item()
        
        return item.get_dictionary()

    def _create_offer_dictionary(
        self, 
        response: HtmlResponse, 
        data: Dict,
    ) -> Dict:
        offers = response.css('div[itemprop="offers"]')

        if len(offers) == 0:
            pass # TODO: Throw error.

        offer_objects = []

        for o in offers:
            price = o.css('span[itemprop="price"]::text').get()
            valid_through = o.css('span[itemprop="validThrough"]::text').get()
            offer_objects.append(
                offer.Offer(price=float(price), valid_until=valid_through)
            )

        offer_objects.sort(key=lambda x: x.price)

        amount = offer_objects[0].price
        valid_until = offer_objects[0].valid_until
        item = offer_item_loader.OfferItemLoader(response=response) \
            .add_store_id(store_id=self.store_id) \
            .add_sold_by(sold_by=self.sold_by) \
            .add_amount(
                amount=str(amount),
            ).add_currency(currency=curreny.Currency.CAD.value) \
            .add_availability(
                availability=availability.Availability.IN_STOCK.value,
            ).add_condition(condition=condition.Condition.NEW.value) \
            .load_item()

        return item.get_dictionary()
