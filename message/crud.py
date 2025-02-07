from typing import Optional

from fastapi import status, HTTPException

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.message import Message
from core.models.user import User
from message.schemas import MessageUpdateCond


async def create_message(session: AsyncSession,
                         message: Message):
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def delete_message_by_id(session: AsyncSession,
                               message_id: int):
    stmt = await session.execute(select(Message).where(Message.id==message_id))
    message = stmt.scalars().first()

    if message:
        session.delete(message)
        await session.commit()
        return {'message': 'Item delete'}
    else:
        raise HTTPException(status_code=404, detail="Message not found")

async def get_message_by_id(session: AsyncSession,
                            message_id: int):
     stmt = await session.execute(select(Message).options(joinedload(Message.user)).where(Message.id == message_id))
     message = stmt.scalar_one_or_none()

     if message:
         return message
     else:
         raise HTTPException(status_code=404, detail="Message not found")


async def update_message(message_id: int, session: AsyncSession, ms_update: MessageUpdateCond) -> Optional[Message]:
    stmt = select(Message).where(Message.id == message_id)

    result = await session.execute(stmt)
    message = result.scalars().first()

    if message:
        message.condition = ms_update.condition
        session.add(message)
        await session.commit()
        return message
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
