from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.crud import get_current_user
from core.models.db_helper import db_helper
from message.schemas import MessageModelId, MessageModel, MessageUpdateMess, MessageItem
from core.models.message import Message as msgCRUD
from user.schemas import User
import message.crud as mess


router = APIRouter(prefix='/message', tags=['Message'])


@router.post('/create/', response_model=MessageModelId)
async def create_message(user: User = Depends(get_current_user),
                         msg: MessageModel = None,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    message = msgCRUD(
        user_id = user.id,
        message = msg.message,
        item_id=msg.item_id
    )
    return await mess.create_message(message=message, session=session)


@router.get('/{message_id}/', response_model=MessageModelId)
async def get_message(message_id: int,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await mess.get_message_by_id(message_id=message_id, session=session)


@router.get('/', response_model=list[MessageItem])
async def get_all(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    messages = await mess.get_all_mess(session=session)

    return [
        {
            "id": msg.id,
            "message": msg.message,
            "user_id": msg.user_id,
            'username': msg.user.username if msg.user else 'Не указано',
            "item_id": msg.item_id,
            'item_name': msg.item.name if msg.item else 'Не указано',
            "created_at": msg.created_at.isoformat() if msg.created_at else "Не указано"
        }
        for msg in messages
    ]


@router.delete('/{message_id}/', response_model=dict)
async def delete_message(message_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await mess.delete_message_by_id(session=session, message_id=message_id)
