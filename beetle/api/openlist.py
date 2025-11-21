from fastapi import APIRouter, Body

from beetle.client import OpenListClient
from beetle.settings import OPENLIST_HOST, OPENLIST_TOKEN


router = APIRouter()


@router.post("/list")
async def list(
    path: str = Body(),
    page: int | None = Body(default=None),
    per_page: int | None = Body(default=None),
    password: str | None = Body(default=None),
    refresh: bool = Body(default=False),
):
    async with OpenListClient(host=OPENLIST_HOST, token=OPENLIST_TOKEN) as client:
        response = await client.list(
            path,
            page=page,
            per_page=per_page,
            password=password,
            refresh=refresh,
        )
        return response
