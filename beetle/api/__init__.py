from fastapi import APIRouter

from beetle.api import task


router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


router.include_router(task.router, prefix="/task", tags=["任务"])
