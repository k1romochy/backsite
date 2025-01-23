from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from user.schemas import UserModel, UserCreate
from user import crud as user


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=list[UserModel])
async def get_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user.get_users(session=session)


@router.post('/create_user/', response_model=UserModel)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user.create_user(user=user_in, session=session)


@router.get('/{user_id}/', response_model=UserModel)
async def get_user(user_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user.get_user(user_id=user_id, session=session)
