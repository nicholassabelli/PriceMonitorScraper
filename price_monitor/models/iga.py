
import ast
import datetime
import logging
import json
import re
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
    region,
    store,
    universal_product_code,
)
from scrapy.utils.project import get_project_settings

class IGA(store.Store):
    store_id = 'iga'
    store_name = 'IGA'
    sold_by = 'Sobeys Inc.'
    region = region.Region.CANADA.value
    domain = 'iga.net'
    allowed_domains = [domain]
    version = get_project_settings().get('VERSION_PRODUCT_DATA_IGA')
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'price_monitor.pipelines.IGAStripAmountPipeline': 300,
            'price_monitor.pipelines.breadcrumb_tags_pipeline.BreadcrumbTagsPipeline': 800,
            # 'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            'price_monitor.pipelines.mongo_db_pipeline.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
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

        data = self._find_json_data(response)
        
        if data:
            return self._create_product_dictionary(response, data)

        logging.warning('No product data found!')
        return None

    def _determine_language_from_url(self, url: str) -> str:
        if re.search(f'www.{self.domain}/en/product/', url):
            return language.Language.EN.value
        elif re.search(f'www.{self.domain}/fr/produit/', url):
            return language.Language.FR.value
        
        return None

    def _determine_availability(self, data: Dict) -> str:
        return availability.Availability.IN_STOCK.value if data \
            else availability.Availability.OUT_OF_STOCK.value

    def _find_json_data(self, response: HtmlResponse) -> Optional[Dict]:
        css_path = "div.product-details.js-ga-productdetails > " + \
           "div.relative::attr(data-product)"

        product_data = response.css(css_path).extract()

        if not product_data:
            logging.error('Unable to load JSON data.') # TODO: Log URL.
            return None

        try:
            return json.loads(product_data[0])
        except:
            pass

        # try:
        #     return ast.literal_eval(product_data[0])
        # except:
        #     pass

        try:
            data = product_data[0].replace("'", '"')
            return json.loads(data)
        except:
            logging.error('Unable to load JSON data.')

    def _create_product_dictionary(
        self, 
        response: HtmlResponse, 
        data: Optional[Dict] = None,
    ) -> product.Product:
        try:
            upc = (
                universal_product_code.UniversalProductCode(
                    upc=data.get('ProductId').replace('_', '')
                )
            ).value
        except:
            # TODO: Log issue and return nothing.
            return None

        title1 = response.css(
                    'meta[property="og:title"]::attr(content)'
                ).extract()[0].split('|')[0]
        title2 = response.css('title::text').get()
        name = title1 or title2

        if not name:
            pass # TODO: Log error and return none.
        elif name == 'Grocery Product' or name == 'Produit épicerie en ligne':
            pass # TODO: Log error and return none.

        brand = data.get('BrandName')

        if not name:
            pass # TODO: Log error and return none.

        item_loader = product_item_loader.ProductItemLoader(
            response=response
        ).add_name(
            response=response,
            name=name, # TODO: What about if it's none.
            language=self.language,
        ).add_brand(
            response=response,
            brand=brand, # TODO: What about if it's none.
            language=self.language,
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
        ).add_supported_language(language=self.language)

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
        breadcrumbs = response.css(
            'ul.nav.breadcrumb \
                > li[itemtype="http://data-vocabulary.org/Breadcrumb"] \
                > a[itemprop="url"] \
                > span[itemprop="title"]::text'
        ).getall()

        item = product_data_item_loader \
            .ProductDataItemLoader(response=response) \
            .add_language_data(
                response=response,
                brand=brand,
                images=response.css(
                    'meta[property="og:image"]::attr(content)'
                ).extract(),
                name=name,
                url=response.url,
                breadcrumbs=breadcrumbs
            ).add_sku(sku=upc) \
            .add_upc(response=response, upc=upc) \
            .add_store_id(store_id=self.store_id) \
            .add_sold_by(sold_by=self.sold_by) \
            .add_version(version=self.version) \
            .load_item()

        return item.get_dictionary()

    def _create_offer_dictionary(
        self, 
        response: HtmlResponse, 
        data: Optional[Dict] = None,
    ) -> Dict:
        amount = str(data.get('SalesPrice') or data.get('RegularPrice')),

        if not amount:
            pass # TODO: If unable to find amount then log and return nothing.

        # TODO: Add valid until.
        item = offer_item_loader.OfferItemLoader(response=response) \
            .add_store_id(store_id=self.store_id) \
            .add_sold_by(sold_by=self.sold_by) \
            .add_amount(
                amount=amount,
            ).add_currency(currency=curreny.Currency.CAD.value) \
            .add_availability(
                availability=availability.Availability.IN_STOCK.value,
            ).add_condition(condition=condition.Condition.NEW.value) \
            .load_item()

        return item.get_dictionary()