from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst
from w3lib.html import replace_entities, replace_escape_chars, remove_tags
from price_monitor.items import product_data
from price_monitor.item_loaders import product_item_loader
from scrapy.http.response.html import HtmlResponse

class ProductDataItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, replace_escape_chars, product_item_loader.remove_latin_space, replace_entities)
    default_output_processor = TakeFirst()
    default_item_class = product_data.ProductData
    name_in = Identity()
    # name_out = Identity()
    description_in = Identity()
    # description_out = Identity()
    gtin_in = Identity()
    supported_languages_in = Identity()
    images_out = Identity()

    def add_name(self, response: HtmlResponse, name: str, language: str):
        self.add_value(
            field_name=product_data.ProductData.KEY_NAME,
            value=self._create_text_field(
                response=response,
                value=name,
                language=language,
            ),
        )

    # def _create_text_field(
    #     self, 
    #     response: HtmlResponse, 
    #     value: str, 
    #     language: str,
    # ) -> Dict[str, Dict[str, str]]:
    #     item_loader = text_item_loader.TextItemLoader(response=response)
    #     item_loader.add_value(text.Text.KEY_LANGUAGE, language)
    #     item_loader.add_value(text.Text.KEY_VALUE, value)

    #     return {
    #         language: dict(item_loader.load_item())
    #     }



    # item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_URL,
    #         value=response.url,
    #     )
    #     item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_NAME,
    #         value=self._create_text_field(
    #             response=response,
    #             value=name,
    #             language=self.language,
    #         ),
    #     )
    #     item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_SKU, 
    #         value=sku,
    #     )
    #     item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_SOLD_BY,
    #         value=self.sold_by,
    #     )
    #     item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_STORE_ID, 
    #         value=self.store_id,
    #     )
    #     item_loader.add_value(
    #         field_name=product_data.ProductData.KEY_SUPPORTED_LANGUAGES,
    #         value=self._create_supported_languages_field(self.language),
    #     )      

    #     if brand:
    #         item_loader.add_value(
    #             field_name=product_data.ProductData.KEY_BRAND,
    #             value=brand,
    #         )

    #     # TODO: Desc.
    #     if description:
    #         item_loader.add_value(
    #             field_name=product_data.ProductData.KEY_DESCRIPTION,
    #             value=description,
    #         )
    #         pass

    #     if upc:
    #         item_loader.add_value(
    #             field_name=product_data.ProductData.KEY_GTIN,
    #             value=self._create_gtin_field(
    #                 response=response,
    #                 type=global_trade_item_number \
    #                     .GlobalTradeItemNumber.UPCA.value,
    #                 value=upc,
    #             ),
    #         )

    #     if model_number:
    #         item_loader.add_value(
    #             field_name=product_data.ProductData.KEY_MODEL_NUMBER,
    #             value=model_number,
    #         )

    #     if images:  
    #         item_loader.add_value(
    #             field_name=product_data.ProductData.KEY_IMAGES,
    #             value=images,
    #         )

