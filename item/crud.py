from fastapi import status

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.item import Item


async def create_item(item: Item, session: AsyncSession):
    session.add(item)

    await session.commit()


async def delete_item_by_id(item_id: int, session: AsyncSession):
    stmt = select(Item).where(Item.id == item_id)
    await session.delete(stmt)
    await session.commit()


async def get_items(session: AsyncSession):
    stmt = select(Item).order_by(Item.id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return items


async def update_item_quantity(item_id: int, session: AsyncSession, new_quantity: int):
    item = select(Item).where(Item.id == item_id)

    item.quantity = new_quantity
    await session.commit()


