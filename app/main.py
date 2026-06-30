from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import execute_router, health_router, runtimes_router
from services import init_pool
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield


app = FastAPI(lifespan=lifespan)

app.state.limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.include_router(health_router)
app.include_router(execute_router)
app.include_router(runtimes_router)
