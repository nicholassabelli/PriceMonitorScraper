# -*- coding: utf-8 -*-

import logging
from scrapy.spiders import Spider, SitemapSpider
from scrapy.loader import ItemLoader
from price_monitor.items import Price, Product, PriceItemLoader, IGAProductItemLoader
from price_monitor.models import Currency

class IGA:
    allowed_domains = ['iga.net']
    custom_settings = {
        'ITEM_PIPELINES': {
    #         'price_monitor.pipelines.TagsPipeline': 300,
            'price_monitor.pipelines.IGAStripAmountPipeline': 300,
            'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            
        }
    }

    def parse_product(self, response):
        productLoader = IGAProductItemLoader(response=response)
        productLoader.add_css(Product.KEY_NAME, ['h1.product-detail__name'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_css(Product.KEY_BRAND, ['span.product-detail__brand'])
        productLoader.add_xpath(Product.KEY_TAGS, '//ul[contains(concat(" ", normalize-space(@class), " "), " breadcrumb ")]/li[last()-1]/a/@href')
        productLoader.add_value(Product.KEY_UPC, [response.url])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = PriceItemLoader(response=response)
        priceLoader.add_css(Price.KEY_AMOUNT, ['#body_0_main_1_ListOfPrices span.price[itemprop=price]'])
        priceLoader.add_value(Price.KEY_CURRENCY, [Currency.CAD])
        return dict(priceLoader.load_item())

class IGASitemapSpider(SitemapSpider):
    name = 'iga_sitemap_spider'
    allowed_domains = IGA.allowed_domains
    custom_settings = IGA.custom_settings
    sitemap_urls = ['http://www.iga.net/robots.txt']
    sitemap_rules = [
        ('/en/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(IGASitemapSpider, self).__init__(*a, **kw)
        self.iga = IGA()

    def parse_product(self, response):
        return self.iga.parse_product(response)

class IGASpider(Spider):
    name = 'iga_spider'
    allowed_domains = IGA.allowed_domains
    custom_settings = IGA.custom_settings
    start_urls = [
        # 'https://www.iga.net/en/product/yop-yogurt-drinkraspberry/00000_000000005692001202',
        # 'https://www.iga.net/en/product/yop-yogurt-drinkblueberry/00000_000000005692001210',
        'https://www.iga.net/en/product/yop-yogurt-drinkblueberry/00000_000000005692001210',
        # 'https://www.iga.net/en/product/chocolate-milk1-/00000_000000005587210518',
        # 'https://www.iga.net/en/product/cheesemarble-cheddar/00000_000000006810090189'
    ]

    def __init__(self, *a, **kw):
        super(IGASpider, self).__init__(*a, **kw)
        self.iga = IGA()

    def parse(self, response):
        return self.iga.parse_product(response)