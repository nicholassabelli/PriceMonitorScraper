# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import Spider, SitemapSpider
from scrapy.loader import ItemLoader
from price_monitor.items import PriceItemLoader, ProductItemLoader

class TheSource:
    allowed_domains = ['thesource.ca']
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.BestBuyTagsPipeline': 300,
        }
    }

    def parse_product(self, response):
        productLoader = ProductItemLoader(response=response)

        productLoader.add_css('name', ['title'])
        productLoader.add_css('description', ['head > meta[name="description"]::attr(content)'])
        productLoader.add_value('currentPrice', [self.__get_price(response)])
        productLoader.add_value('url', [response.url])
        productLoader.add_css('availability', ['div.availability-text::attr(content)'])
        productLoader.add_css('tags', ['head > meta[name="keywords"]::attr(content)'])
        productLoader.add_css('upc', ['div.product-details-numbers-wrapper > div:nth-child(2)'])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = PriceItemLoader(response=response)
        priceLoader.add_css('amount', ['#addToCartForm > input[name="price"]::attr(value)'])
        priceLoader.add_css('currency', ['section.pdp-section > meta[itemprop="priceCurrency"]::attr(content)'])
        return dict(priceLoader.load_item())

class TheSourceSitemapSpider(SitemapSpider):
    name = 'the_source_sitemap_spider'
    allowed_domains = TheSource.allowed_domains
    custom_settings = TheSource.custom_settings
    sitemap_urls = ['http://www.thesource.ca/robots.txt']
    sitemap_rules = [
        ('/en-ca/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(TheSourceSitemapSpider, self).__init__(*a, **kw)
        self.the_source = TheSource()

    def parse_product(self, response):
        return self.the_source.parse_product(response)

class TheSourceSpider(Spider):
    name = 'the_source_spider'
    allowed_domains = TheSource.allowed_domains
    custom_settings = TheSource.custom_settings
    start_urls = [
        'https://www.bestbuy.ca/en-ca/product/spider-man-ps4/10439890.aspx',
    ]

    def __init__(self, *a, **kw):
        super(TheSourceSpider, self).__init__(*a, **kw)
        self.the_source = TheSource()

    def parse(self, response):
        return self.the_source.parse_product(response)

# 75x75
# twobyone > div.at-total-container > div:nth-child(1) > img

# 500x500
# #pagecontent > div > div.prod-detail-wrapper.jmvc-controller-pdp.ng-scope.pdp_desktop.pdp_ui > div > div.prod-detail-bot > div > div.prod-detail-assets.span7 > div.core-utilities > div > div:nth-child(2) > div > div.gallery-image-container > div > div:nth-child(2) > img