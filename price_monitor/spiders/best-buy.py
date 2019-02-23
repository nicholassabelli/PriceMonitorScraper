# -*- coding: utf-8 -*-

import logging, json, re
from scrapy.spiders import Spider, SitemapSpider
from scrapy.loader import ItemLoader
from price_monitor.items import PriceItemLoader, ProductItemLoader

class BestBuy:
    allowed_domains = ['bestbuy.ca']
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.TagsPipeline': 300,
        }
    }

    def parse_product(self, response):
        # texts = response.xpath('//script/text()')[0].re(".*brand.*")
        texts = response.xpath('//script/text()')

        for text in texts:
            match = text.re(".*var data_layer =.*")

            if match:
                # strip = match[0].strip()
                # split = match[0].strip().split('var data_layer =')[1].split(';')
                # split = split[1].split(';')
                brand = json.loads(match[0].strip().split('var data_layer =')[1].split(';')[0])['brand']
                # logging.info(brand)
                # MISCELLANEOUS
            
        productLoader = ProductItemLoader(response=response)
        productLoader.add_css('name', ['head > meta[property="og:title"]::attr(content)'])
        productLoader.add_css('description', ['head > meta[name="description"]::attr(content)'])
        productLoader.add_css('releaseDate', ['#ctl00_CP_ctl00_PD_lblReleaseDate'])
        productLoader.add_value('currentPrice', [self.__get_price(response)])
        productLoader.add_value('url', [response.url])
        productLoader.add_css('availability', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > link[itemprop="availability"]::attr(href)'])
        productLoader.add_css('tags', ['head > meta[name="keywords"]::attr(content)'])
        # productLoader.add_css('brand', ['div[data-brand-bar]::attr(data-brand-bar)'])
        productLoader.add_value('brand', [brand])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = PriceItemLoader(response=response)
        priceLoader.add_css('amount', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > meta[itemprop="price"]::attr(content)'])
        priceLoader.add_css('currency', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > meta[itemprop="priceCurrency"]::attr(content)'])
        return dict(priceLoader.load_item())

class BestBuySitemapSpider(SitemapSpider):
    name = 'best_buy_sitemap_spider'
    allowed_domains = BestBuy.allowed_domains
    custom_settings = BestBuy.custom_settings
    sitemap_urls = ['http://www.bestbuy.ca/robots.txt']
    sitemap_rules = [
        ('/en-ca/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(BestBuySitemapSpider, self).__init__(*a, **kw)
        self.best_buy = BestBuy()

    def parse_product(self, response):
        return self.best_buy.parse_product(response)

class BestBuySpider(Spider):
    name = 'best_buy_spider'
    allowed_domains = BestBuy.allowed_domains
    custom_settings = BestBuy.custom_settings
    start_urls = [
        'https://www.bestbuy.ca/en-ca/product/spider-man-ps4/10439890.aspx',
        'https://www.bestbuy.ca/en-ca/product/apple-macbook-pro-with-touch-bar-13-3-space-grey-intel-core-i5-2-3ghz-256gb-8gb-ram-english/12727808.aspx?',
    ]

    def __init__(self, *a, **kw):
        super(BestBuySpider, self).__init__(*a, **kw)
        self.best_buy = BestBuy()

    def parse(self, response):
        return self.best_buy.parse_product(response)

# 75x75
# twobyone > div.at-total-container > div:nth-child(1) > img

# 500x500
# #pagecontent > div > div.prod-detail-wrapper.jmvc-controller-pdp.ng-scope.pdp_desktop.pdp_ui > div > div.prod-detail-bot > div > div.prod-detail-assets.span7 > div.core-utilities > div > div:nth-child(2) > div > div.gallery-image-container > div > div:nth-child(2) > img