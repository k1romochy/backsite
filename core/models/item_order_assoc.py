from sqlalchemy import Table, Column, ForeignKey
from core.models.base import Base

item_order_association = Table(
    "item_order_association",
    Base.metadata,
    Column("order_id", ForeignKey("order.id"), primary_key=True),
    Column("item_id", ForeignKey("item.id"), primary_key=True)
)
