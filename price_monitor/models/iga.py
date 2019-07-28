
# -*- coding: utf-8 -*-

import datetime
from price_monitor.items import Offer, Product
from price_monitor.item_loaders import OfferItemLoader, IGAProductItemLoader
from price_monitor.models import Currency

class IGA:
    store_name = 'IGA'
    sold_by = 'Sobeys Inc.'
    domain = 'iga.net'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.IGAStripAmountPipeline': 300,
            'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            'price_monitor.pipelines.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response):
        productLoader = IGAProductItemLoader(response=response)
        productLoader.add_value(Product.KEY_STORE, [self.store_name])
        productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_css(Product.KEY_NAME, ['h1.product-detail__name'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_css(Product.KEY_BRAND, ['span.product-detail__brand'])
        productLoader.add_xpath(Product.KEY_TAGS, ['//ul[contains(concat(" ", normalize-space(@class), " "), " breadcrumb ")]/li[last()-1]/a/@href'])
        productLoader.add_value(Product.KEY_UPC, [response.url])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = OfferItemLoader(response=response)
        priceLoader.add_css(Offer.KEY_AMOUNT, ['#body_0_main_1_ListOfPrices span.price[itemprop=price]'])
        priceLoader.add_value(Offer.KEY_CURRENCY, [Currency.CAD.value])
        priceLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        return dict(priceLoader.load_item())