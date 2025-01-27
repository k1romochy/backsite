from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils as auth_utils
from fastapi import APIRouter, Depends, Form, HTTPException, status

from core.models.db_helper import db_helper
from user.schemas import User
from auth.jwt_model import Token
from user.crud import get_user_by_username


router = APIRouter(prefix='/jwt', tags=['JWT'])


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')

    user = await get_user_by_username(username=username, session=session)
    if not user:
        raise unauthed_exc

    if auth_utils.validate_password(password=password,
                                    hashed_password=user.password):
        return user


@router.post('/login/', response_model=Token)
async def auth_user_jwt(user: User = Depends):
    jwt_payload = {
        'sub': user.id,
        'username': user.username,
        'email': user.email
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return Token(access_token=token, token_type='Bearer')
