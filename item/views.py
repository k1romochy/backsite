from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt_auth import get_current_user
from core.models.db_helper import db_helper
from item.schemas import ItemCreate, ItemModel, Item
from item import crud as item
from user.schemas import User

router = APIRouter(prefix='/items', tags=['Items'])


@router.get('/', response_model=list[Item])
async def get_items(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.get_items(session=session)


@router.post('/create_item/', response_model=ItemCreate)
async def create_item(item_in: ItemCreate, current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    item_in_dict = item_in.model_dump()
    item_in_dict['user_id'] = current_user.id
    item_in_with_user_id = ItemCreate(**item_in_dict)
    return await item.create_item(item=item_in_with_user_id, session=session)


@router.get('/{item_id}/', response_model=Item)
async def get_item(item_id: int,
                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.get_item(item_id=item_id, session=session)


@router.post('/{item_id}/update/', response_model=Item)
async def update_item(item_id: int, new_quantity: int,
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.update_item_quantity(item_id=item_id, new_quantity=new_quantity, session=session)


@router.get('/{item_id}/user/', response_model=Item)
async def get_item_with_user(item_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.get_item_with_user(item_id=item_id, session=session)


@router.delete('/{item_id}/', response_model=Item)
async def delete_item(item_id: int,
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await item.delete_item_by_id(item_id=item_id, session=session)
