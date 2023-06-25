from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)  # immutable dataclass with no behavior
class OrderLine:
    id: str
    sku: str
    quantity: int


@dataclass
class Batch:
    def __init__(self, ref: str, sku: str, quantity: int, eta: Optional[datetime]):
        self.reference = ref
        self.sku = sku
        self.quantity = quantity
        self.eta = eta

    def allocate(self, order_line: OrderLine):
        self.quantity -= order_line.quantity

    def can_allocate(self, order_line: OrderLine) -> bool:
        if self.quantity < order_line.quantity:
            return False
        if self.sku != order_line.sku:
            return False
        return True
