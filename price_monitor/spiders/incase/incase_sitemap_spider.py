from scrapy.spiders import SitemapSpider
from price_monitor.models.incase import Incase

class LeonsSitemapSpider(SitemapSpider):
    name = 'incase_sitemap_spider'
    allowed_domains = Incase.allowed_domains
    custom_settings = Incase.custom_settings
    sitemap_urls = ['http://www.incasedesigns.ca/robots.txt']
    sitemap_rules = [
        ('/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(LeonsSitemapSpider, self).__init__(*a, **kw)
        self.incase = Incase()

    def parse_product(self, response):
        return self.incase.parse_product(response)

