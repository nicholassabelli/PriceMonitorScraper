from __future__ import annotations
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from price_monitor.items import offer

class OfferItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()
    default_item_class = offer.Offer

    def add_amount(self, amount: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_AMOUNT,
            value=amount,
        )
        return self

    def add_availability(self, availability: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_AVAILABILITY,
            value=availability,
        )
        return self

    def add_condition(self, condition: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_CONDITION,
            value=condition,
        )
        return self

    def add_currency(self, currency: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_CURRENCY,
            value=currency,
        )
        return self

    def add_end_date(self, end_date: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_END_DATE,
            value=end_date,
        )
        return self

    def add_sold_by(self, sold_by: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_SOLD_BY,
            value=sold_by,
        )
        return self

    def add_store_id(self, store_id: str) -> OfferItemLoader:
        self.add_value(
            field_name=offer.Offer.KEY_STORE_ID,
            value=store_id,
        )
        return self