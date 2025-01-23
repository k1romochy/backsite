from fastapi import status

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.item import Item
from item.schemas import ItemCreate


async def create_item(item: ItemCreate, session: AsyncSession) -> None:
    item_db = Item(**item.model_dump())
    session.add(item_db)

    await session.commit()
    await session.refresh(item_db)
    return item_db


async def delete_item_by_id(item_id: int, session: AsyncSession) -> None:
    stmt = select(Item).where(Item.id == item_id)
    await session.delete(stmt)
    await session.commit()


async def get_items(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return items


async def update_item_quantity(item_id: int, session: AsyncSession, new_quantity: int) -> None:
    item = select(Item).where(Item.id == item_id)

    item.quantity = new_quantity
    await session.commit()


async def get_item(item_id: int, session: AsyncSession) -> Item:
    stmt = select(Item).where(Item.id == item_id)
    result: Result = await session.execute(stmt)
    item = result.scalar()

    return item
