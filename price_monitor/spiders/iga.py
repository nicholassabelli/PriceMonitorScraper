# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import Spider, SitemapSpider
from scrapy.loader import ItemLoader
from price_monitor.items import PriceItemLoader, ProductItemLoader

class IGA:
    allowed_domains = ['iga.net']
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.BestBuyTagsPipeline': 300,
        }
    }

    def parse_product(self, response):
        productLoader = ProductItemLoader(response=response)

        productLoader.add_css('name', ['head > meta[property="og:title"]::attr(content)'])
        productLoader.add_css('description', ['head > meta[name="description"]::attr(content)'])
        productLoader.add_css('releaseDate', ['#ctl00_CP_ctl00_PD_lblReleaseDate'])
        productLoader.add_value('currentPrice', [self.__get_price(response)])
        productLoader.add_value('url', [response.url])
        productLoader.add_css('availability', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > link[itemprop="availability"]::attr(href)'])
        productLoader.add_css('tags', ['head > meta[name="keywords"]::attr(content)'])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = PriceItemLoader(response=response)
        priceLoader.add_css('amount', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > meta[itemprop="price"]::attr(content)'])
        priceLoader.add_css('currency', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > meta[itemprop="priceCurrency"]::attr(content)'])
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
        'https://www.iga.net/en/product/yop-yogurt-drinkblueberry/00000_000000005692001210',
    ]

    def __init__(self, *a, **kw):
        super(IGASpider, self).__init__(*a, **kw)
        self.iga = IGA()

    def parse(self, response):
        return self.iga.parse_product(response)