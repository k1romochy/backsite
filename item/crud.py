from typing import Optional

from fastapi import status, HTTPException

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.user import User
from core.models.item import Item
from item.schemas import ItemUpdateRequest


async def create_item(item: Item, session: AsyncSession) -> Item:
    session.add(item)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item_by_id(item_id: int, session: AsyncSession):
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()

    if item:
        await session.delete(item)
        await session.commit()
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


async def get_items(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return items


async def update_item(item_id: int, session: AsyncSession, item_update: ItemUpdateRequest) -> Optional[Item]:
    stmt = select(Item).where(Item.id == item_id)

    result = await session.execute(stmt)
    item = result.scalars().first()

    if item:
        item.quantity = item_update.quantity
        item.condition = item_update.condition
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


async def get_item_with_user(item_id: int, session: AsyncSession):
    stmt = select(Item).options(selectinload(Item.users)).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if item is not None:
        return item.users
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

async def assign_user(item_id: int, user_id: int, session: AsyncSession):
    stmt = select(Item).options(selectinload(Item.users)).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    stmt = select(User).where(User.id == user_id)
    user_result = await session.execute(stmt)
    user = user_result.scalar_one_or_none()

    if not item or not user:
        raise HTTPException(status_code=404, detail="User or Item not found")

    if user in item.users:
        raise HTTPException(status_code=400, detail="User already assigned to item")

    item.users.append(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error while assigning user")

    return {'message': 'Success'}


async def unassign_user(item_id: int, user_id: int, session: AsyncSession):
    stmt = select(Item).options(selectinload(Item.users)).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    stmt = select(User).where(User.id == user_id)
    user_result = await session.execute(stmt)
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user not in item.users:
        raise HTTPException(status_code=400, detail="User is not assigned to this item")

    item.users.remove(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error while unassigning user")

    return {'message': 'Success'}
