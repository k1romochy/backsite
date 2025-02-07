from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.crud import get_current_user
from core.models.db_helper import db_helper
from message.schemas import MessageModelId, MessageModel, MessageUpdateCond
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
        message =  msg.message,

    )
    return await mess.create_message(message=message, session=session)


@router.get('/{message_id}/', response_model=MessageModelId)
async def get_message(message_id: int,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await mess.get_message_by_id(message_id=message_id, session=session)


@router.patch('/{message_id}/')
async def update_msg(message_id: int,
                     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                     message_update: MessageUpdateCond = None):
    return await mess.update_message(message_id=message_id, session=session, ms_update=message_update)
