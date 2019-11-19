from price_monitor.items import (
    offer,
    product
)
from price_monitor.models import (
    universal_product_code
)
from price_monitor.pipelines import (
    price_monitor_pipeline
)

class UniversalProductCodePipeline(price_monitor_pipeline.PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(product.Product.KEY_UPC):
            try:
                upc = universal_product_code.UniversalProductCode(item[product.FieldProduct.KEY_UPC]).value # TODO: Check for nulls in mongodb pipeline.
            except:
                upc = None

        item[product.Product.KEY_UPC] = upc
        item[product.Product.KEY_CURRENT_OFFER][offer.Offer.KEY_SKU] = upc
        item[product.Product.KEY_MODEL_NUMBER] = upc
        item[product.Product.KEY_SKU] = upc

        return item