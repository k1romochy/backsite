from dotenv import load_dotenv
import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from os import getenv

load_dotenv()


class AuthJWT(BaseModel):
    private_path_key: Path = Path('auth/jwt-private.pem')
    public_path_key: Path = Path('auth/jwt-public.pem')
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    db_url: str = os.getenv('POSTGRES_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
