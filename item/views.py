from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from core.models.item import Item
from item.schemas import ItemCreate, ItemModel
from item import crud as item

router = APIRouter(prefix='/items', tags=['Items'])


@router.get('/', response_model=list[ItemModel])
async def get_items(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.get_items(session=session)


@router.post('/create_item/', response_model=ItemModel)
async def create_item(item_in: ItemCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.create_item(item=item_in, session=session)


@router.get('/{item_id}/', response_model=ItemModel)
async def get_item(item_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await item.get_item(item_id=item_id, session=session)
