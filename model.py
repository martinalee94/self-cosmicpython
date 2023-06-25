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
        self.reference: str = ref
        self.sku: str = sku
        self._purchased_quantity: int = quantity
        self.eta: Optional[datetime] = eta
        self._allocations: set[OrderLine] = set()

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line=order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        if self._purchased_quantity < order_line.quantity:
            return False
        if self.sku != order_line.sku:
            return False
        return True

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
