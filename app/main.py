from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import execute_router, health_router, runtimes_router
from services import init_pool
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield


app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.include_router(health_router)
app.include_router(execute_router)
app.include_router(runtimes_router)
