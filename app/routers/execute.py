from fastapi import APIRouter, HTTPException
from models import ExecuteRequest, ExecuteResponse
from services import execute_cpp, execute_java, execute_js, execute_python, sandbox

router = APIRouter()

_handlers = {
    "python": execute_python,
    "javascript": execute_js,
    "cpp": execute_cpp,
    "java": execute_java,
}


@router.post("/execute", response_model=ExecuteResponse)
async def execute(req: ExecuteRequest) -> ExecuteResponse:
    handler = _handlers[req.language]
    try:
        async with sandbox() as (box_id, box_dir, meta_path):
            return await handler(box_id, box_dir, meta_path, req.code, req.stdin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
