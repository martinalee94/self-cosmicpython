from datetime import date, timedelta
import pytest
from model import OrderLine, Batch

# from model import ...

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def make_batch_and_line(sku, batch_quantity, line_quantity):
    return (
        Batch("batch-001", sku, batch_quantity, eta=date.today()),
        OrderLine("order-123", sku, line_quantity),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    # GIVEN
    line = OrderLine(order_id="Order-001", sku="SMALL-TABLE", quantity=2)
    batch = Batch(ref="batch-001", sku="SMALL-TABLE", quantity=20, eta=today)

    # WHEN
    batch.allocate(order_line=line)

    # THEN
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    # GIVEN
    large_batch, small_line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=20, line_quantity=1
    )

    # WHEN
    result = large_batch.can_allocate(order_line=small_line)

    # THEN
    assert result is True


def test_cannot_allocate_if_available_smaller_than_required():
    # GIVEN
    small_batch, large_line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=2, line_quantity=10
    )

    # WHEN
    result = small_batch.can_allocate(order_line=large_line)

    # THEN
    assert result is False


def test_can_allocate_if_available_equal_to_required():
    # GIVEN
    batch, line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=20, line_quantity=20
    )

    # WHEN
    result = batch.can_allocate(order_line=line)

    # THEN
    assert result is True


def test_cannot_allocate_if_skus_do_not_match():
    # GIVEN
    line = OrderLine(order_id="Order-001", sku="SMALL-TABLE", quantity=2)
    batch = Batch(ref="batch-001", sku="BIG-TABLE", quantity=20, eta=today)

    # WHEN
    result = batch.can_allocate(order_line=line)

    # THEN
    assert result is False
