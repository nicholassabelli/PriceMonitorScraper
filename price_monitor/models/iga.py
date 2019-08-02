
# -*- coding: utf-8 -*-

import datetime
from price_monitor.items import Offer, Product, Store
from price_monitor.item_loaders import OfferItemLoader, IGAProductItemLoader, StoreItemLoader
from price_monitor.models import Availability, Condition, Currency, Region

class IGA:
    store_id = 'iga'
    store_name = 'IGA'
    sold_by = 'Sobeys Inc.'
    region = Region.CANADA.value
    domain = 'iga.net'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.IGAStripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            'price_monitor.pipelines.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response):
        productLoader = IGAProductItemLoader(response=response)
        # productLoader.add_value(Product.KEY_STORE, [self.store_name])
        # productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        # productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_css(Product.KEY_NAME, ['h1.product-detail__name'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_css(Product.KEY_BRAND, ['span.product-detail__brand'])
        # productLoader.add_xpath(Product.KEY_TAGS, ['//ul[contains(concat(" ", normalize-space(@class), " "), " breadcrumb ")]/li[last()-1]/a/@href'])
        productLoader.add_value(Product.KEY_UPC, [response.url])
        productLoader.add_value(Product.KEY_STORE, self.__get_store(response))
        return productLoader.load_item()

    def __get_price(self, response):
        offerLoader = OfferItemLoader(response=response)
        offerLoader.add_css(Offer.KEY_AMOUNT, ['#body_0_main_1_ListOfPrices span.price[itemprop=price]'])
        # offerLoader.add_value(Offer.KEY_AVAILABILITY, Availability.IN_STOCK.value)
        offerLoader.add_value(Offer.KEY_CURRENCY, [Currency.CAD.value])
        offerLoader.add_value(Offer.KEY_CONDITION, Condition.NEW.value)
        offerLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        offerLoader.add_value(Offer.KEY_SOLD_BY, [self.sold_by])
        offerLoader.add_value(Offer.KEY_STORE_ID, [self.store_id])
        return dict(offerLoader.load_item())

    def __get_store(self, response):
        storeLoader = StoreItemLoader(response=response)
        storeLoader.add_value(Store.KEY_DOMAIN, [self.domain])
        storeLoader.add_value(Store.KEY_ID, [self.store_id])
        storeLoader.add_value(Store.KEY_NAME, [self.store_name])
        storeLoader.add_value(Store.KEY_REGION, self.region)
        return dict(storeLoader.load_item())