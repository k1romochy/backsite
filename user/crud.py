from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from core.models.user import User
from user.schemas import UserCreate


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    user_db = User(**user.model_dump())
    session.add(user_db)

    await session.commit()
    await session.refresh(user_db)
    return user_db


async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
