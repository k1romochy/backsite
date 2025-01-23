from fastapi import status

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.user import User


async def create_user(user: User, session: AsyncSession) -> None:
    session.add(user)

    await session.commit()


async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def delete_user_by_id(session: AsyncSession, user_id: int) -> None:
    stmt = select(User).where(User.id == user_id)
    await session.delete(stmt)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        return user
    else:
        return status.HTTP_404_NOT_FOUND
