from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class OrderLine:
    id:str
    sku:str
    quantity:int
    
@dataclass
class Batch:
    def __init__(self, ref:str, sku:str, q: int, eta:Optional[datetime]):
        self.reference = ref
        self.sku = sku
        self.quantity = q
        self.eta = eta
        
    def allocate(self,order_line: OrderLine):
        order_line.quantity -= self.quantity
    