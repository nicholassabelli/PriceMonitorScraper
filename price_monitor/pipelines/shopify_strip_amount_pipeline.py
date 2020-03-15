from price_monitor.items import (
    offer
)
from price_monitor.items import (
    product
)
from price_monitor.pipelines import (
    strip_amount_pipeline
)

class ShopifyStripAmountPipeline(strip_amount_pipeline.StripAmountPipeline):
    def process_item(self, item, spider):
        if item.get(product.Product.KEY_CURRENT_OFFER) and item.get(product.Product.KEY_CURRENT_OFFER).get(offer.Offer.KEY_AMOUNT):
            item[product.Product.KEY_CURRENT_OFFER][offer.Offer.KEY_AMOUNT] = float(item[product.Product.KEY_CURRENT_OFFER][offer.Offer.KEY_AMOUNT].strip('$')) / 100
        
        return item