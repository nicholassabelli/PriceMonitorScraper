from scrapy.spiders import SitemapSpider
from price_monitor.models.leons import Leons

class LeonsSitemapSpider(SitemapSpider):
    name = 'leons_sitemap_spider'
    allowed_domains = Leons.allowed_domains
    custom_settings = Leons.custom_settings
    sitemap_urls = ['http://www.leons.ca/robots.txt']
    sitemap_rules = [
        ('/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(LeonsSitemapSpider, self).__init__(*a, **kw)
        self.leons = Leons()

    def parse_product(self, response):
        return self.leons.parse_product(response)

