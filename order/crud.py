from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from core.models.order import Order
from core.models.item import Item


async def create_order(session: AsyncSession, order: Order, item_ids: list[int]):
    session.add(order)
    await session.flush()

    if item_ids:
        items_query = await session.execute(select(Item).where(Item.id.in_(item_ids)))
        items = items_query.scalars().all()

        if len(items) != len(item_ids):
             await session.rollback()
             raise HTTPException(status_code=404, detail="Один или несколько товаров не найдены")

        order.items = items
    await session.commit()
    await session.refresh(order)
    return order


async def get_order_by_id(order_id: int, session: AsyncSession):
    query = await session.execute(select(Order).where(Order.id == order_id))
    order = query.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail='Order not found')
    return order


async def get_all_orders(session: AsyncSession):
    query = await session.execute(select(Order))
    return query.scalars().all()


async def delete_order_by_id(session: AsyncSession, order_id: int):
    order = await get_order_by_id(order_id=order_id, session=session)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    await session.delete(order)
    await session.commit()
    return {'message': 'Order deleted successfully'}