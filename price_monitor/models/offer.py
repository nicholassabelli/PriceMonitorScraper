from typing import Optional, TypedDict

# class Offer(TypedDict, total=False):
class Offer():
    def __init__(self, price: float, valid_until: Optional[str] = None):
        self.price = price
        self.valid_until = valid_until
    
    def __repr__(self):
        return repr((self.price, self.valid_until))