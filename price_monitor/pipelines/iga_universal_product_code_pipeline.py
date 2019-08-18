# -*- coding: utf-8 -*-

from price_monitor.items import Offer, Product
from price_monitor.models import UniversalProductCode
from price_monitor.pipelines.universal_product_code_pipeline import UniversalProductCodePipeline

class IGAUniversalProductCodePipeline(UniversalProductCodePipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_UPC):
            upc = UniversalProductCode(item[Product.KEY_UPC].split('_')[1]).value
            item[Product.KEY_UPC] = upc
            item[Product.KEY_CURRENT_OFFER][Offer.KEY_SKU] = upc
            item[Product.KEY_MODEL_NUMBER] = upc
            item[Product.KEY_SKU] = upc
        
        return item