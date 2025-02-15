from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.crud import get_current_user
from core.models.db_helper import db_helper
from core.models.request import Request as RequestCRUD
from request.schemas import RequestBase, RequestDep, RequestModelId, RequestBase, RequestUpdateCond
from user.schemas import User
import request.crud as req


router = APIRouter(prefix='/request', tags=['Request'])


@router.post('/create/', response_model=RequestModelId)
async def create_message(
    user: User = Depends(get_current_user),
    request_data: RequestBase = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    if not request_data.item_id:
        raise HTTPException(status_code=400, detail="item_id is required")

    request = RequestCRUD(
        user_id=user.id,
        item_id=request_data.item_id
    )

    return await req.create_request(request=request, session=session)


@router.get('/{request_id}/', response_model=RequestModelId)
async def get_request(request_id: int,
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await req.get_request_by_id(request_id=request_id, session=session)


@router.get('/', response_model=list[RequestDep])
async def get_all(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    requests = await req.get_all_req(session=session)

    return [
        {
            "id": request.id,
            "user_id": request.user_id,
            'username': request.user.username if request.user else 'Не указано',
            "item_id": request.item_id,
            'item_name': request.item.name if request.item else 'Не указано',
            "condition": request.condition
        }
        for request in requests
    ]


@router.patch('/{request_id}/', response_model=RequestModelId)
async def update_request_condition(
    request_id: int,
    update_data: RequestUpdateCond,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await req.updatecond(request_id=request_id, new_cond=update_data.condition, session=session)


@router.delete('/{request_id}/', response_model=dict)
async def delete_request(request_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await req.delete_request_by_id(session=session, request_id=request_id)

