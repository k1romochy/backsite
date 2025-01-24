from multiprocessing.managers import Value
from typing import Optional

from fastapi import status, HTTPException

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.item import Item
from item.schemas import ItemCreate

async def create_item(item: ItemCreate, session: AsyncSession) -> Item:
    item_db = Item(**item.model_dump())
    session.add(item_db)

    await session.commit()
    await session.refresh(item_db)
    return item_db


async def delete_item_by_id(item_id: int, session: AsyncSession) -> None:
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if item is not None:
        await session.delete(stmt)
        await session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


async def get_items(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return items


async def update_item_quantity(item_id: int, session: AsyncSession, new_quantity: int) -> Optional[Item]:
    stmt = select(Item).where(Item.id == item_id)

    result = await session.execute(stmt)
    item = result.scalars().first()

    if item:
        item.quantity = new_quantity
        session.add(item)
        await session.commit()
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


async def get_item(item_id: int, session: AsyncSession) -> Item:
    stmt = select(Item).where(Item.id == item_id)
    result: Result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if item is not None:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


async def get_item_with_user(item_id: int, session: AsyncSession) -> Item:
    stmt = select(Item).options(joinedload(Item.user)).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if item is not None:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
