# -*- coding: utf-8 -*-

import logging
from scrapy.spiders import Spider, SitemapSpider
from scrapy.loader import ItemLoader
from price_monitor.items import Price, Product, PriceItemLoader, MetroProductItemLoader
from price_monitor.models import Currency

class Metro:
    store_name = 'Metro'
    allowed_domains = ['metro.ca']
    custom_settings = {
    }

    def parse_product(self, response):
        productLoader = MetroProductItemLoader(response=response)
        productLoader.add_css(Product.KEY_NAME, ['h1.pi--title'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_css(Product.KEY_BRAND, ['div.pi--brand'])
        productLoader.add_css(Product.KEY_WEIGHT_OR_VOLUME, ['div.pi--weight'])
        productLoader.add_css(Product.KEY_TAGS, ['ul.b--list > li > a > span[itemprop="name"]'])
        productLoader.add_css(Product.KEY_UPC, ['span[itemprop="sku"]'])
        productLoader.add_css(Product.KEY_DESCRIPTION, ['span[itemprop="description"]'])
        # TODO: Fix need to verify the accordion item.
        # #content-temp > div.grid--container.pb-20 > div > div:nth-child(3) > div > p
        # To get the ingredients.
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = PriceItemLoader(response=response)
        priceLoader.add_css(Price.KEY_AMOUNT, ['#content-temp > div.grid--container.pt-20 > div.product-info.item-addToCart > div.pi--middle-col > div.pi--prices > div:nth-child(1) > div.pi--prices--first-line::attr(data-main-price)'])
        priceLoader.add_value(Price.KEY_CURRENCY, [Currency.CAD])
        return dict(priceLoader.load_item())

class MetroSitemapSpider(SitemapSpider):
    name = 'metro_sitemap_spider'
    allowed_domains = Metro.allowed_domains
    custom_settings = Metro.custom_settings
    sitemap_urls = ['https://www.metro.ca/robots.txt']
    sitemap_rules = [
        ('/en/online-grocery/aisles/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(MetroSitemapSpider, self).__init__(*a, **kw)
        self.metro = Metro()

    def parse_product(self, response):
        return self.metro.parse_product(response)

class MetroSpider(Spider):
    name = 'metro_spider'
    allowed_domains = Metro.allowed_domains
    custom_settings = Metro.custom_settings
    start_urls = [
        'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/yogurt/drinkable-yogurts/2-raspberry-flavoured-drinkable-yogurt/p/056920012029',
        'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/milk-cream/flavoured-milk/1-chocolate-milk/p/068700106361',
        'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/milk-cream/1-skim-milk/1-milk/p/055872700114',
    ]

    def __init__(self, *a, **kw):
        super(MetroSpider, self).__init__(*a, **kw)
        self.metro = Metro()

    def parse(self, response):
        return self.metro.parse_product(response)