from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy_utils import database_exists, create_database

from api.routers import router
from api.db.base import Base, engine
from api.db.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database_exists(settings.DATABASE_URL_syncpg):
        create_database(settings.DATABASE_URL_syncpg)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(title="ProductsApp",lifespan=lifespan)

app.include_router(router)
