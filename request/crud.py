from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models.request import Request


async def create_request(session: AsyncSession, request: Request):
    session.add(request)
    await session.commit()
    await session.refresh(request)
    return request


async def delete_requests_by_id(session: AsyncSession,
                                request_id: int):
    stmt = await session.execute(select(Request).where(Request.id==request_id))
    message = stmt.scalars().first()

    if message:
        await session.delete(message)
        await session.commit()
        return {'message': 'Item delete'}
    else:
        raise HTTPException(status_code=404, detail="Message not found")


async def get_request_by_id(session: AsyncSession,
                            request_id: int):
        stmt = await session.execute(select(Request).options(joinedload(Request.user)).where(Request.id == request_id))
        request = stmt.scalar_one_or_none()

        if request:
           return request
        else:
           raise HTTPException(status_code=404, detail="Message not found")


async def get_all_req(session: AsyncSession):
    stmt = await session.execute(select(Request).options(selectinload(Request.item), selectinload(Request.user)))

    requests = stmt.scalars().all()
    return requests


async def updatecond(request_id: int, new_cond: str, session: AsyncSession):
    result = await session.execute(select(Request).where(Request.id == request_id))
    request = result.scalar_one_or_none()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.condition = new_cond
    await session.commit()
    await session.refresh(request)
    return request


async def delete_request_by_id(session: AsyncSession, request_id: int):
    request = await get_request_by_id(request_id=request_id, session=session)
    if not request:
        raise HTTPException(status_code=404, detail='Order not found')

    await session.delete(request)
    await session.commit()
    return {'message': 'Order deleted successfully'}

