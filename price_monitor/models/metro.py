# -*- coding: utf-8 -*-

import datetime
from price_monitor.items import Offer, Product, Store
from price_monitor.item_loaders import OfferItemLoader, MetroProductItemLoader, StoreItemLoader
from price_monitor.models import Availability, Condition, Currency, Region

class Metro:
    store_id = 'metro'
    store_name = 'Metro'
    sold_by = 'Metro Inc.' #'Metro Richelieu Inc.'
    region = Region.CANADA.value
    domain = 'metro.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.StripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            'price_monitor.pipelines.UniversalProductCodePipeline': 900,
            'price_monitor.pipelines.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response):
        productLoader = MetroProductItemLoader(response=response)
        productLoader.add_css(Product.KEY_NAME, ['h1.pi--title'])
        productLoader.add_value(Product.KEY_CURRENT_OFFER, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_css(Product.KEY_BRAND, ['div.pi--brand'])
        productLoader.add_css(Product.KEY_WEIGHT_OR_VOLUME, ['div.pi--weight'])
        # productLoader.add_css(Product.KEY_TAGS, ['ul.b--list > li > a > span[itemprop="name"]'])
        productLoader.add_css(Product.KEY_UPC, ['span[itemprop="sku"]'])
        productLoader.add_css(Product.KEY_DESCRIPTION, ['span[itemprop="description"]'])
        # TODO: Fix need to verify the accordion item.
        # #content-temp > div.grid--container.pb-20 > div > div:nth-child(3) > div > p
        # To get the ingredients.
        productLoader.add_value(Product.KEY_STORE, self.__get_store(response))
        return productLoader.load_item()

    def __get_price(self, response):
        offerLoader = OfferItemLoader(response=response)
        offerLoader.add_css(Offer.KEY_AMOUNT, ['#content-temp > div.grid--container.pt-20 > div.product-info.item-addToCart > div.pi--middle-col > div.pi--prices > div:nth-child(1) > div.pi--prices--first-line::attr(data-main-price)'])
        offerLoader.add_value(Offer.KEY_AVAILABILITY, Availability.IN_STOCK.value)
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
