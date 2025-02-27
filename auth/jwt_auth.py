import os
import uuid

import jwt
from dotenv import load_dotenv
from jwt import ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Form, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPAuthorizationCredentials
from auth import utils as auth_utils
from auth.crud import validate_auth_user, create_session, delete_session, get_current_user
from core.models.db_helper import db_helper
from core.models.user import User
from auth.jwt_model import Token
from user.crud import get_user_by_username
from user.schemas import UserModel

router = APIRouter(prefix='/auth', tags=['auth'])
COOKIE_SESSION_ID_KEY = 'session_id'


@router.post("/login/", response_model=Token)
async def auth_user_jwt(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await get_user_by_username(username=username, session=session)

    if not user or not auth_utils.validate_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    jwt_payload = {"sub": user.username, "user_id": user.id, "email": user.email}
    token = auth_utils.encode_jwt(jwt_payload)

    session_id = str(uuid.uuid4())
    await create_session(user.id, session_id, session)

    response.set_cookie(key=COOKIE_SESSION_ID_KEY, value=session_id, httponly=True, secure=False, samesite='lax')

    return Token(access_token=token, token_type="Bearer")


@router.get('/me/')
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return {'username': current_user.username,
            'user_id': current_user.id}


@router.post("/logout/")
async def logout(
        response: Response,
        session_id: str = Cookie(None),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    if session_id:
        await delete_session(session_id, session)

    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}
