from fastapi import status

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.user import User
from user.schemas import UserCreate


async def create_user(user: UserCreate, session: AsyncSession) -> None:
    session.add(user)

    await session.commit()


async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        return user
    else:
        return status.HTTP_404_NOT_FOUND
