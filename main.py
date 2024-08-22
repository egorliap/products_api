from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routers import router
from api.db.base import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(title="ProductsApp",lifespan=lifespan)

app.include_router(router)
