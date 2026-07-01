from fastapi import APIRouter, Request
from limiter import limiter

router = APIRouter()


@router.get("/health")
@limiter.limit("10/minute")
def health(request: Request):
    return {"status": "healthy"}
