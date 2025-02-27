import uvicorn

from fastapi import FastAPI, Body, Path
from fastapi.middleware.cors import CORSMiddleware

from app.gen_router import router as general_router
from user.views import router as user_router
from item.views import router as item_router
from auth.jwt_auth import router as auth_router
from message.views import router as mess_router
from request.views import router as request_router
from order.views import router as order_router

from core.models.base import Base
from core.models.db_helper import db_helper
from core.config import settings

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan = lifespan)


app.include_router(user_router)
app.include_router(general_router)
app.include_router(item_router)
app.include_router(auth_router)
app.include_router(mess_router)
app.include_router(request_router)
app.include_router(order_router)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def hello_index():
    return {
        'message': 'Hello index'
    }


if __name__ == '__main__':
    uvicorn.run('run:app', host="localhost", port=8000, reload=True)
