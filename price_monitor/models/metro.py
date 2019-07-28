# -*- coding: utf-8 -*-

from price_monitor.items import Offer, Product
from price_monitor.item_loaders import OfferItemLoader, MetroProductItemLoader
from price_monitor.models import Currency

class Metro:
    store_name = 'Metro'
    allowed_domains = ['metro.ca']
    custom_settings = {
    }

    def parse_product(self, response):
        productLoader = MetroProductItemLoader(response=response)
        productLoader.add_css(Product.KEY_NAME, ['h1.pi--title'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_css(Product.KEY_BRAND, ['div.pi--brand'])
        productLoader.add_css(Product.KEY_WEIGHT_OR_VOLUME, ['div.pi--weight'])
        productLoader.add_css(Product.KEY_TAGS, ['ul.b--list > li > a > span[itemprop="name"]'])
        productLoader.add_css(Product.KEY_UPC, ['span[itemprop="sku"]'])
        productLoader.add_css(Product.KEY_DESCRIPTION, ['span[itemprop="description"]'])
        # TODO: Fix need to verify the accordion item.
        # #content-temp > div.grid--container.pb-20 > div > div:nth-child(3) > div > p
        # To get the ingredients.
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = OfferItemLoader(response=response)
        priceLoader.add_css(Offer.KEY_AMOUNT, ['#content-temp > div.grid--container.pt-20 > div.product-info.item-addToCart > div.pi--middle-col > div.pi--prices > div:nth-child(1) > div.pi--prices--first-line::attr(data-main-price)'])
        priceLoader.add_value(Offer.KEY_CURRENCY, [Currency.CAD.value])
        return dict(priceLoader.load_item())
