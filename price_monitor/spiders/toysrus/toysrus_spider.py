from scrapy.http import Request
from scrapy.spiders import Spider
from price_monitor.models.toysrus import Toysrus

class ToysrusSpider(Spider):
    name = 'toysrus_spider'
    allowed_domains = Toysrus.allowed_domains
    custom_settings = Toysrus.custom_settings
    start_urls = [
        # 'https://www.toysrus.ca/en/Star-Wars-The-Vintage-Collection-The-Mandalorian-AT-ST-Raider-Vehicle-with-Figure/7489BAB1.html',
        # 'https://www.toysrus.ca/en/Star-Wars-The-Black-Series-The-Mandalorian-6-inch-Scale-Collectible--063061/3AC65FDE.html',
        'https://www.toysrus.ca/en/Star-Wars-The-Black-Series-Rey-and-D-O-6-inch-Scale--The-Rise-of-Skywalker-Collectible--063061/3AC65BDE.html',
        # 'https://www.toysrus.ca/en/Star-Wars-The-Vintage-Collection-Star-Wars--The-Empire-Strikes-Back-Cave-of-Evil-Special/DBF0E448.html',
        # 'https://www.toysrus.ca/en/Star-Wars-The-Black-Series-6-inch-General-Veers---R-Exclusive/D41878CA.html',
    ]

    def __init__(self, *a, **kw):
        super(ToysrusSpider, self).__init__(*a, **kw)
        self.toysrus = Toysrus()
        
    def parse(self, response):
        return self.toysrus.parse_product(response)