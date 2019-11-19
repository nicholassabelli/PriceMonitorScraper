from price_monitor.items.offer import Offer
from price_monitor.items.product import Product
from price_monitor.models.availability import Availability
from price_monitor.pipelines.strip_amount_pipeline import StripAmountPipeline

class IGAStripAmountPipeline(StripAmountPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_CURRENT_OFFER) and item.get(Product.KEY_CURRENT_OFFER).get(Offer.KEY_AMOUNT):
            item[Product.KEY_CURRENT_OFFER][Offer.KEY_AMOUNT] = float(item[Product.KEY_CURRENT_OFFER][Offer.KEY_AMOUNT].strip('$'))
            item[Product.KEY_CURRENT_OFFER][Offer.KEY_AVAILABILITY] = Availability.IN_STOCK.value
        else:
            item[Product.KEY_CURRENT_OFFER][Offer.KEY_AVAILABILITY] = Availability.OUT_OF_STOCK.value
        
        return item