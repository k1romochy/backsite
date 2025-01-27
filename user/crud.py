from typing import Type, Sequence

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from core.models.user import User
from user.schemas import UserCreate
import auth.utils as auth_utils


async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def get_user_by_id(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_user_with_items(user_id: int, session: AsyncSession) -> User:
    stmt = select(User).options(selectinload(User.items)).where(User.id == user_id)
    result = await session.execute(stmt)

    user = result.scalar_one_or_none()
    if user is not None:
        return user
    else:
        raise ValueError('User with this id not found')


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)

    user = result.scalar_one_or_none()
    if user is not None:
        return user
    else:
        raise ValueError('User with this id not found')


async def registrate_user(user: UserCreate, session: AsyncSession):
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail='User  with this username already exists')

    user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    user_db = User(**user.model_dump())

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db
