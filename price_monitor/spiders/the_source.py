from scrapy.spiders import Spider
from price_monitor.models.the_source import TheSource

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