# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.spiders import SitemapSpider
from price_monitor.models.walmart import Walmart

class WalmartSitemapSpider(SitemapSpider):
    name = 'walmart_sitemap_spider'
    allowed_domains = Walmart.allowed_domains
    custom_settings = Walmart.custom_settings
    sitemap_urls = ['https://www.walmart.ca/robots.txt']
    sitemap_rules = [
        ('/en/ip/.*star-wars', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(WalmartSitemapSpider, self).__init__(*a, **kw)
        self.walmart = Walmart()

    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url, self._parse_sitemap, meta={'js_global_variable': 'window.__PRELOADED_STATE__'})

    def parse_product(self, response):
        return self.walmart.parse_product(response)