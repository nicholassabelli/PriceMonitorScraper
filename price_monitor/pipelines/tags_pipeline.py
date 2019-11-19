from price_monitor.items import (
    product
)
from price_monitor.pipelines import (
    price_monitor_pipeline
)

class TagsPipeline(price_monitor_pipeline.PriceMonitorPipeline):
    def process_item(self, item, spider):
        if item.get(product.Product.KEY_TAGS):
            item[product.Product.KEY_TAGS] = item[product.Product.KEY_TAGS].split(',')
        
        return item