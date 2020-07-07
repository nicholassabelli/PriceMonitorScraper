from urllib.parse import unquote
from price_monitor.items import (
    language_data,
    product,
    product_data,
)
from price_monitor.helpers import (
    item_loader_helper,
)
from price_monitor.pipelines import tags_pipeline
from scrapy.utils.project import get_project_settings

class BreadcrumbTagsPipeline(tags_pipeline.TagsPipeline):
    breadcrumb_blocklist = get_project_settings().get('BREADCRUMB_BLOCKLIST')

    def process_item(self, item, spider):
        supported_languages = item.get(
            product.Product.KEY_SUPPORTED_LANGUAGES
        )
        lang = list(supported_languages)[0]
        store_seller_key = list(item.get(product.Product.KEY_PRODUCT_DATA))[0]

        breadcrumbs = item \
            .get(product.Product.KEY_PRODUCT_DATA) \
            .get(store_seller_key) \
            .get(product_data.ProductData.KEY_LANGUAGE_DATA) \
            .get(language_data.LanguageData.KEY_BREADCRUMBS)

        if store_seller_key and breadcrumbs and lang:
            breadcrumbs_dictionary = dict.fromkeys(breadcrumbs, True)

            for _, value in enumerate(self.breadcrumb_blocklist):
                # ['', 'en', 'online_grocery', 'browse', 'in_the_community']:
                breadcrumbs_dictionary.pop(value, None)

            breadcrumbs = list(breadcrumbs_dictionary.keys())
            item[product.Product.KEY_TAGS] = list(map(
                lambda x : item_loader_helper.ItemLoaderHelper._create_text_field(response=None, value=x, language=lang), 
                breadcrumbs,
            ))

            item[product.Product.KEY_PRODUCT_DATA][store_seller_key][
                product_data.ProductData.KEY_LANGUAGE_DATA
            ][
                language_data.LanguageData.KEY_BREADCRUMBS
            ] = ' > '.join(breadcrumbs)

        # if item.get(product.Product.KEY_TAGS):
        #     # item[Product.KEY_TAGS] = unquote(item[Product.KEY_TAGS]).split('/')

        #     for _, value in self.breadcrumb_blocklist.items():
        #         # ['', 'en', 'online_grocery', 'browse', 'in_the_community']:
        #         if item[product.Product.KEY_TAGS].get(value):
        #             item[product.Product.KEY_TAGS].remove(value)

        return item


