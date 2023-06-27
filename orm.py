from sqlalchemy.orm import mapper
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey

import model

metadata = MetaData()

# Define db tables and columns with SQLAlchemy
# Now it's perfectly fine to switch to different ORM
order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("eta", DateTime(), nullable=True),
    Column("_purchased_quantity", Integer, nullable=False),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    # ORM imports the domain model
    # Domain model doesn't rely on ORM anymore
    lines_mapper = mapper(model.OrderLine, order_lines)
    batches_mapper = mapper(model.Batch, batches)
