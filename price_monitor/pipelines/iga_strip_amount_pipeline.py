# -*- coding: utf-8 -*-

from price_monitor.items import Offer, Product
from price_monitor.models import Availability
from price_monitor.pipelines.strip_amount_pipeline import StripAmountPipeline

class IGAStripAmountPipeline(StripAmountPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_CURRENT_PRICE) and item.get(Product.KEY_CURRENT_PRICE).get(Offer.KEY_AMOUNT):
            item[Product.KEY_CURRENT_PRICE][Offer.KEY_AMOUNT] = float(item[Product.KEY_CURRENT_PRICE][Offer.KEY_AMOUNT].strip('$'))
            item[Product.KEY_AVAILABILITY] = Availability.IN_STOCK.value
        else:
            item[Product.KEY_AVAILABILITY] = Availability.OUT_OF_STOCK.value
        
        return item