# -*- coding: utf-8 -*-

from price_monitor.items import Offer, Product
from price_monitor.models import UniversalProductCode
from price_monitor.pipelines.price_monitor_pipeline import PriceMonitorPipeline

class UniversalProductCodePipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_UPC):
            try:
                upc = UniversalProductCode(item[Product.KEY_UPC]).value # TODO: Check for nulls in mongodb pipeline.
            except:
                upc = None

        item[Product.KEY_UPC] = upc
        item[Product.KEY_CURRENT_OFFER][Offer.KEY_SKU] = upc
        item[Product.KEY_MODEL_NUMBER] = upc
        item[Product.KEY_SKU] = upc

        return item