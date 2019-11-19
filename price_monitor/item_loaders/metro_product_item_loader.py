from scrapy.loader.processors import Identity
from price_monitor.item_loaders import product_item_loader

class MetroProductItemLoader(product_item_loader.ProductItemLoader):
    tags_out = Identity()