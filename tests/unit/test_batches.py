from datetime import date, timedelta
import pytest
from model import OrderLine, Batch

# from model import ...

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    # GIVEN
    order = OrderLine(id="Order-001", sku="SMALL-TABLE", quantity=2)
    batch = Batch(ref="batch-001", sku="SMALL-TABLE", quantity=20, eta=today)

    # WHEN
    batch.allocate(order_line=order)

    # THEN
    assert batch.quantity == 18
