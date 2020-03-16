from scrapy.http import Request
from scrapy.spiders import Spider
from price_monitor.models.leons import Leons

class LeonsSpider(Spider):
    name = 'leons_spider'
    allowed_domains = Leons.allowed_domains
    custom_settings = Leons.custom_settings
    start_urls = [
        # 'https://www.leons.ca/products/sony-65-4k-hdr-smart-120hz-led-tv-xbr65x950g?variant=15940800118830',
        'https://www.leons.ca/products/sony-65-4k-hdr-android-smart-xr240-led-tv-xbr65x800h?variant=31644334194734',
        'https://fr.leons.ca/products/sony-65-4k-hdr-android-smart-xr240-led-tv-xbr65x800h?variant=31644334194734',
    ]

    def __init__(self, *a, **kw):
        super(LeonsSpider, self).__init__(*a, **kw)
        self.leons = Leons()

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url, dont_filter=True, meta={'js_global_variable': 'window.Shopify'})

    def parse(self, response):
        return self.leons.parse_product(response)