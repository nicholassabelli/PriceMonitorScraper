
import datetime
from price_monitor.items import (
    offer,
    product,
    store_item
)
from price_monitor.item_loaders import (
    offer_item_loader,
    iga_product_item_loader,
    store_item_loader
)
from price_monitor.models import (
    availability,
    condition,
    curreny,
    region
)

class IGA:
    store_id = 'iga'
    store_name = 'IGA'
    sold_by = 'Sobeys Inc.'
    region = region.Region.CANADA.value
    domain = 'iga.net'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.IGAStripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            'price_monitor.pipelines.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response):
        productLoader = iga_product_item_loader.IGAProductItemLoader(response=response)
        # productLoader.add_value(Product.KEY_STORE, [self.store_name])
        # productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        # productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_css(product.Product.KEY_NAME, ['h1.product-detail__name'])
        productLoader.add_value(product.Product.KEY_CURRENT_OFFER, [self.__get_price(response)])
        productLoader.add_value(product.Product.KEY_URL, [response.url])
        productLoader.add_css(product.Product.KEY_BRAND, ['span.product-detail__brand'])
        # productLoader.add_xpath(Product.KEY_TAGS, ['//ul[contains(concat(" ", normalize-space(@class), " "), " breadcrumb ")]/li[last()-1]/a/@href'])
        productLoader.add_value(product.Product.KEY_UPC, [response.url])
        productLoader.add_value(product.Product.KEY_STORE, self.__get_store(response))
        return productLoader.load_item()

    def __get_price(self, response):
        offerLoader = offer_item_loader.OfferItemLoader(response=response)
        offerLoader.add_css(offer.Offer.KEY_AMOUNT, ['#body_0_main_1_ListOfPrices span.price[itemprop=price]'])
        # offerLoader.add_value(Offer.KEY_AVAILABILITY, Availability.IN_STOCK.value)
        offerLoader.add_value(offer.Offer.KEY_CURRENCY, curreny.Currency.CAD.value)
        offerLoader.add_value(offer.Offer.KEY_CONDITION, condition.Condition.NEW.value)
        offerLoader.add_value(offer.Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        offerLoader.add_value(offer.Offer.KEY_SOLD_BY, [self.sold_by])
        offerLoader.add_value(offer.Offer.KEY_STORE_ID, [self.store_id])
        return dict(offerLoader.load_item())

    def __get_store(self, response):
        storeLoader = store_item_loader.StoreItemLoader(response=response)
        storeLoader.add_value(store_item.StoreItem.KEY_DOMAIN, [self.domain])
        storeLoader.add_value(store_item.StoreItem.KEY_ID, [self.store_id])
        storeLoader.add_value(store_item.StoreItem.KEY_NAME, [self.store_name])
        storeLoader.add_value(store_item.StoreItem.KEY_REGION, self.region)
        return dict(storeLoader.load_item())