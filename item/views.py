from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from item.schemas import Item
from item import crud as item

router = APIRouter(prefix='/items', tags=['Items'])


@router.get('/', response_model=list[Item])
async def get_items(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.get_items(session=session)


@router.post('/create_user/', response_model=Item)
async def create_items(item_in: Item, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.create_item(item=item_in, session=session)


@router.get('/{user_id}/', response_model=User)
async def get_user(item: Item = Depends(item.get_item)):
    return item
