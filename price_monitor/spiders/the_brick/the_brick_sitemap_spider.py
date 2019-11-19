from scrapy.spiders import SitemapSpider
from price_monitor.models.the_brick import TheBrick

class TheBrickSitemapSpider(SitemapSpider):
    name = 'the_brick_sitemap_spider'
    allowed_domains = TheBrick.allowed_domains
    custom_settings = TheBrick.custom_settings
    sitemap_urls = ['http://www.thebrick.com/robots.txt']
    sitemap_rules = [
        ('/products/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(TheBrickSitemapSpider, self).__init__(*a, **kw)
        self.the_brick = TheBrick()

    def parse_product(self, response):
        return self.the_brick.parse_product(response)

