from typing import Sequence, Type

from fastapi import status

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.user import User
from user.schemas import UserModel, UserCreate


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    new_user = User(name=user.name,
                    email=user.email,
                    role=user.role,
                    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> Type[User]:
    user = await session.get(User, user_id)
    if user:
        return user
    else:
        return status.HTTP_404_NOT_FOUND
