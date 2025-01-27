import os
import jwt
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth import utils as auth_utils
from auth.utils import get_private_key, get_public_key
from core.config import settings
from core.models.db_helper import db_helper
from user.schemas import User
from auth.jwt_model import Token
from user.crud import get_user_by_username
from jose import JWTError

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = settings.auth_jwt.algorithm

router = APIRouter(prefix='/jwt', tags=['JWT'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt/login/")


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await get_user_by_username(username=username, session=session)

    if not user or not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    return user


@router.post('/login/', response_model=Token)
async def auth_user_jwt(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await validate_auth_user(username=username, password=password, session=session)
    jwt_payload = {
        'sub': user.id,
        'username': user.username,
        'email': user.email
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return Token(access_token=token, token_type='Bearer')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    algorithm: str | None = 'RS256',
    public_key: str | None = None
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    algorithm = algorithm or settings.auth_jwt.algorithm
    public_key = public_key or get_public_key()

    try:
        payload = jwt.decode(token, public_key, algorithms=[algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user
