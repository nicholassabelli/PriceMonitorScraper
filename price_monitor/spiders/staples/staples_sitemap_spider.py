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

# 75x75
# twobyone > div.at-total-container > div:nth-child(1) > img

# 500x500
# #pagecontent > div > div.prod-detail-wrapper.jmvc-controller-pdp.ng-scope.pdp_desktop.pdp_ui > div > div.prod-detail-bot > div > div.prod-detail-assets.span7 > div.core-utilities > div > div:nth-child(2) > div > div.gallery-image-container > div > div:nth-child(2) > img