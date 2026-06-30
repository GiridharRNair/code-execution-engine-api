from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import execute_router, health_router
from services import init_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(execute_router)
