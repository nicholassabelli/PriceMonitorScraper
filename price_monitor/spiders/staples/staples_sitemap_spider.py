# -*- coding: utf-8 -*-

from scrapy.spiders import SitemapSpider
from price_monitor.models.staples import Staples

class StaplesSitemapSpider(SitemapSpider):
    name = 'staples_sitemap_spider'
    allowed_domains = Staples.allowed_domains
    custom_settings = Staples.custom_settings
    sitemap_urls = ['https://www.staples.ca/robots.txt']
    sitemap_rules = [
        ('/en-ca/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(StaplesSitemapSpider, self).__init__(*a, **kw)
        self.staples = Staples()

    def parse_product(self, response):
        return self.staples.parse_product(response)