from scrapy.spiders import SitemapSpider
from price_monitor.models.toysrus import Toysrus

class ToysrusSitemapSpider(SitemapSpider):
    name = 'toysrus_sitemap_spider'
    allowed_domains = Toysrus.allowed_domains
    custom_settings = Toysrus.custom_settings
    sitemap_urls = ['http://www.toysrus.ca/robots.txt']
    sitemap_rules = [
        ('/en/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(ToysrusSitemapSpider, self).__init__(*a, **kw)
        self.toysrus = Toysrus()

    def parse_product(self, response):
        return self.toysrus.parse_product(response)

