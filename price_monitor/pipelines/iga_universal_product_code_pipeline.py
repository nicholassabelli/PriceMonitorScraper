# -*- coding: utf-8 -*-

from price_monitor.items import Product
from price_monitor.models import UniversalProductCode
from price_monitor.pipelines.universal_product_code_pipeline import UniversalProductCodePipeline

class IGAUniversalProductCodePipeline(UniversalProductCodePipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_UPC):
            item[Product.KEY_UPC] = UniversalProductCode(item[Product.KEY_UPC].split('_')[1]).value
        
        return item