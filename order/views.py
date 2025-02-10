from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Item
from core.models.db_helper import db_helper
from core.models.order import Order as OrderCRUD
from order.schemas import OrderModel, OrderModelId
import order.crud as ord
from auth.crud import get_current_user
from user.schemas import UserModel

router = APIRouter(prefix='/order', tags=['Orders'])


@router.post('/create/', response_model=OrderModelId)
async def create_order(
        order_data: OrderModel,
        user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    order = OrderCRUD(
        user_id=user.id,
        name=order_data.name,
        cost=order_data.cost
    )

    return await ord.create_order(
        session=session,
        order=order,
        item_ids=order_data.items
    )


@router.get('/{order_id}/', response_model=OrderModelId)
async def get_order(order_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await ord.get_order_by_id(order_id=order_id, session=session)


@router.get('/', response_model=list[OrderModelId])
async def get_all_orders(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await ord.get_all_orders(session=session)


@router.delete('/{order_id}/', response_model=dict)
async def delete_order(order_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await ord.delete_order_by_id(session=session, order_id=order_id)
