
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
    product_data
)
from price_monitor.item_loaders import (
    offer_item_loader,
    iga_product_item_loader,
    store_item_loader,
    product_item_loader,
    product_data_item_loader
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

class IGA(store.Store):
    store_id = 'iga'
    store_name = 'IGA'
    sold_by = 'Sobeys Inc.'
    region = region.Region.CANADA.value
    domain = 'iga.net'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'price_monitor.pipelines.IGAStripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            # 'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            'price_monitor.pipelines.mongo_db_pipeline.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response: HtmlResponse) -> Optional[product.Product]:
        self.language = self._determine_language_from_url(response.url)

        if not self.language:
            logging.error('Unable to determine language!')
            return None

        data = self._find_json_data(response)
        
        if data:
            return self.__load_with_dictionary(response, data)

        logging.warning('No product data found!')
        return None

    def _determine_language_from_url(self, url: str) -> str:
        if re.search(f'www.{self.domain}/en/product/', url):
            return language.Language.EN.value
        elif re.search(f'www.{self.domain}/fr/product/', url):
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
            logging.error('Unable to load JSON data.')
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

    def __load_with_dictionary(
        self, 
        response: HtmlResponse, 
        data: Dict,
    ) -> product.Product:
        product_loader = product_item_loader.ProductItemLoader(
            response=response
        )

        try:
            upc = (
                universal_product_code.UniversalProductCode(
                    upc=data.get('ProductId').replace('_', '')
                )
            ).value
        except:
            upc = None

        if upc:
            product_loader.add_value(
                product.Product.KEY_GTIN, 
                value=super()._create_gtin_field(
                    response=response, 
                    type=global_trade_item_number
                        .GlobalTradeItemNumber.UPCA.value, 
                    value=upc
                )
            )

        product_loader.add_value(
            field_name=product.Product.KEY_BRAND, 
            value=data.get('BrandName')
        )
        product_loader.add_value(
            field_name=product.Product.KEY_CURRENT_OFFER, 
            value=self.__create_offer_dictionary(response, data)
        )
        product_loader.add_value(
            field_name=product.Product.KEY_MODEL_NUMBER, 
            value=upc
        )
        product_loader.add_value(
            field_name=product.Product.KEY_PRODUCT_DATA, 
            value=self.__create_product_data_dictionary(response, data, upc)
        )
        product_loader.add_value(
            field_name=product.Product.KEY_STORE, 
            value=self.__create_store_dictionary(response)
        )

        return product_loader.load_item()

    def __create_product_data_dictionary(
        self, 
        response: HtmlResponse, 
        data: Dict, 
        upc: str,
    ) -> Dict:
        return super()._create_product_data_dictionary(
            response=response,
            name=response.css('title::text').get(),
            brand=data.get('BrandName'), 
            upc=upc,
            sku=upc, 
            images=response.css(
                'meta[property="og:image"]::attr(content)'
            ).extract(),
        )

    def __create_offer_dictionary(
        self, 
        response: HtmlResponse, 
        data: Dict,
    ) -> Dict:
        return super()._create_offer_dictionary(
            response=response,
            amount=data.get('SalesPrice') or data.get('RegularPrice'),
            availability=availability.Availability.IN_STOCK.value,
            condition=condition.Condition.NEW.value,
            currency=curreny.Currency.CAD.value,
            sold_by=self.sold_by,
            store_id=self.store_id
        )

    def __create_store_dictionary(self, response: HtmlResponse) -> Dict:
        return super()._create_store_dictionary(
            response=response, 
            domain=self.domain, 
            store_id=self.store_id, 
            store_name=self.store_name, 
            region=self.region
        )

    # def __get_price(self, response):
    #     offerLoader = offer_item_loader.OfferItemLoader(response=response)
    #     offerLoader.add_css(offer.Offer.KEY_AMOUNT, ['#body_0_main_1_ListOfPrices span.price[itemprop=price]'])
    #     # offerLoader.add_value(Offer.KEY_AVAILABILITY, Availability.IN_STOCK.value)
    #     offerLoader.add_value(offer.Offer.KEY_CURRENCY, curreny.Currency.CAD.value)
    #     offerLoader.add_value(offer.Offer.KEY_CONDITION, condition.Condition.NEW.value)
    #     offerLoader.add_value(offer.Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
    #     offerLoader.add_value(offer.Offer.KEY_SOLD_BY, [self.sold_by])
    #     offerLoader.add_value(offer.Offer.KEY_STORE_ID, [self.store_id])
    #     return dict(offerLoader.load_item())

    # def __get_store(self, response):
    #     storeLoader = store_item_loader.StoreItemLoader(response=response)
    #     storeLoader.add_value(store_item.StoreItem.KEY_DOMAIN, [self.domain])
    #     storeLoader.add_value(store_item.StoreItem.KEY_ID, [self.store_id])
    #     storeLoader.add_value(store_item.StoreItem.KEY_NAME, [self.store_name])
    #     storeLoader.add_value(store_item.StoreItem.KEY_REGION, self.region)
    #     return dict(storeLoader.load_item())

            # product_loader = iga_product_item_loader.IGAProductItemLoader(
        #     response=response
        # )

        # # productLoader.add_value(Product.KEY_STORE, [self.store_name])
        # # productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        # # productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        # productLoader.add_css(product.Product.KEY_NAME, ['h1.product-detail__name', 'title'])
        # productLoader.add_value(product.Product.KEY_CURRENT_OFFER, [self.__get_price(response)])
        # productLoader.add_value(product.Product.KEY_URL, [response.url])
        # productLoader.add_css(product.Product.KEY_BRAND, ['span.product-detail__brand'])
        # # productLoader.add_xpath(Product.KEY_TAGS, ['//ul[contains(concat(" ", normalize-space(@class), " "), " breadcrumb ")]/li[last()-1]/a/@href'])
        # productLoader.add_value(product.Product.KEY_UPC, [response.url])
        # productLoader.add_value(product.Product.KEY_STORE, self.__get_store(response))
        # return productLoader.load_item()

        # data['tags'] = self.__parse_tags(data['tags'])


            # # TODO: Define empty method in parent, or with fields that don't change.
    # def _create_product_data_dictionary(self, response: HtmlResponse, data: Dict, upc: str) -> Dict:
    #     # super()._create_product_data_dictionary(response, data, upc)

    #     self.item_loader = \
    #         product_data_item_loader.ProductDataItemLoader(response=response)

    #     if upc:
    #         self.item_loader.add_value(
    #             field_name=product.Product.KEY_GTIN,
    #             value=super()._create_gtin_field(
    #                 response=response,
    #                 type=global_trade_item_number \
    #                     .GlobalTradeItemNumber.UPCA.value,
    #                 value=upc
    #             )
    #         )

    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_URL,
    #         value=response.url
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_NAME,
    #         value=super()._create_text_field(
    #             response=response,
    #             value=response.css('title::text').get(),
    #             language=self.language
    #         )
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_BRAND,
    #         value=data.get('BrandName')
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_SKU, 
    #         value=upc
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_MODEL_NUMBER,
    #         value=upc
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_SOLD_BY,
    #         value=self.sold_by
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_STORE_ID, 
    #         value=self.store_id
    #     )
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_SUPPORTED_LANGUAGES,
    #         value=super()._create_supported_languages_field(self.language)
    #     )        
    #     self.item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_IMAGES,
    #         value=response.css(
    #             'meta[property="og:image"]::attr(content)'
    #         ).extract()
    #     )

    #     return (self.item_loader.load_item()).get_dictionary()