# -*- coding: utf-8 -*-

from scrapy.loader.processors import Identity
from price_monitor.item_loaders.product_item_loader import ProductItemLoader

class MetroProductItemLoader(ProductItemLoader):
    tags_out = Identity()