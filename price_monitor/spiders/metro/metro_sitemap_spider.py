# -*- coding: utf-8 -*-

from scrapy.spiders import SitemapSpider
from price_monitor.models import Metro

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