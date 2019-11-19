from urllib.parse import unquote
from price_monitor.items.product import Product
from price_monitor.pipelines.tags_pipeline import TagsPipeline

class BreadcrumbTagsPipeline(TagsPipeline):
    def process_item(self, item, spider):
        if item.get(Product.KEY_TAGS):
            item[Product.KEY_TAGS] = unquote(item[Product.KEY_TAGS]).split('/')

            for x in ['', 'en', 'online_grocery', 'browse', 'in_the_community']:
                if item.get(x):
                    item.remove(x)

        return item