import datetime
from price_monitor.items import (
    offer,
    product,
    store_item
)
from price_monitor.item_loaders import (
    offer_item_loader,
    metro_product_item_loader,
    store_item_loader
)
from price_monitor.models import (
    availability,
    condition,
    curreny,
    region
)

class Metro:
    store_id = 'metro'
    store_name = 'Metro'
    sold_by = 'Metro Inc.' #'Metro Richelieu Inc.'
    region = region.Region.CANADA.value
    domain = 'metro.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.StripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            'price_monitor.pipelines.UniversalProductCodePipeline': 900,
            'price_monitor.pipelines.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response):
        productLoader = metro_product_item_loader.MetroProductItemLoader(response=response)
        productLoader.add_css(product.Product.KEY_NAME, ['h1.pi--title'])
        productLoader.add_value(product.Product.KEY_CURRENT_OFFER, [self.__get_price(response)])
        productLoader.add_value(product.Product.KEY_URL, [response.url])
        productLoader.add_css(product.Product.KEY_BRAND, ['div.pi--brand'])
        productLoader.add_css(product.Product.KEY_WEIGHT_OR_VOLUME, ['div.pi--weight'])
        # productLoader.add_css(Product.KEY_TAGS, ['ul.b--list > li > a > span[itemprop="name"]'])
        productLoader.add_css(product.Product.KEY_UPC, ['span[itemprop="sku"]'])
        productLoader.add_css(product.Product.KEY_DESCRIPTION, ['span[itemprop="description"]'])
        # TODO: Fix need to verify the accordion item.
        # #content-temp > div.grid--container.pb-20 > div > div:nth-child(3) > div > p
        # To get the ingredients.
        productLoader.add_value(product.Product.KEY_STORE, self.__get_store(response))
        return productLoader.load_item()

    def __get_price(self, response):
        offerLoader = offer_item_loader.OfferItemLoader(response=response)
        offerLoader.add_css(offer.Offer.KEY_AMOUNT, ['#content-temp > div.grid--container.pt-20 > div.product-info.item-addToCart > div.pi--middle-col > div.pi--prices > div:nth-child(1) > div.pi--prices--first-line::attr(data-main-price)'])
        offerLoader.add_value(offer.Offer.KEY_AVAILABILITY, availability.Availability.IN_STOCK.value)
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
