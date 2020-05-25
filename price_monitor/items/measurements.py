from scrapy import (
    Item, 
    Field,
)
from typing import (
    Dict,
)

class Measurements(Item):
    # Array indexes. 
    KEY_LENGTH = 'length'
    KEY_HEIGHT = 'height'
    KEY_WIDTH = 'width'

    # Fields.
    length = Field()
    height = Field()
    width = Field()

    def get_dictionary(self) -> Dict:
        return dict(self)