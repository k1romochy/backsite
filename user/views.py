from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from user.schemas import User
from user import crud as user


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=list[User])
async def get_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    users = await user.get_users(session=session)

    return users


@router.post('/create_user/', response_model=User)
async def create_product(user_in: User, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user.create_user(user=user_in, session=session)


@router.get('/{user_id}/', response_model=User)
async def get_user(user: User = Depends(user.get_user)):
    return user
