# -*- coding: utf-8 -*-

from price_monitor.items import Product
from price_monitor.pipelines.price_monitor_pipeline import PriceMonitorPipeline

class TagsPipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_TAGS):
            item[Product.KEY_TAGS] = item[Product.KEY_TAGS].split(',')
        
        return item