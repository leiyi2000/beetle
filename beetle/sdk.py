from typing import List, Optional, AsyncIterable

import urllib
import logging

import httpx
from pydantic import BaseModel, field_validator


log = logging.getLogger(__name__)


class PathEntry(BaseModel):
    id: str
    path: str
    name: str
    size: int
    is_dir: bool
    modified: str
    created: str
    sign: str
    thumb: str
    type: int


class ListResponse(BaseModel):
    content: List[PathEntry]
    total: int
    readme: str
    provider: str

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, value):
        if value is None:
            return []
        return value


class OpenListClient:
    def __init__(self, host: str, token: str):
        self.host = host
        self.client = httpx.AsyncClient()
        self._headers = {"Authorization": token}

    async def aclose(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | None = None,
        headers: dict | None = None,
        content = None,
        data = None,
    ) -> httpx.Response:
        url = f"{self.host}{path}"
        if headers:
            headers.update(self._headers)
        else:
            headers = self._headers.copy()
        response = await self.client.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            content=content,
            data=data,
        )
        if not (response.is_success or response.json()["code"] == 200):
            log.warning(
                f"Request failed: {method} {url} - {response.status_code} - {response.text}"
            )
        return response

    async def list(
        self,
        path: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        password: Optional[str] = None,
        refresh: bool = False,
    ) -> ListResponse:
        path = path.rstrip("/")
        path = "/" if path == "" else path
        payload = {
            "path": path,
            "page": page,
            "per_page": per_page,
            "password": password,
            "refresh": refresh,
        }
        response = await self._request("POST", "/api/fs/list", json=payload)
        return ListResponse.model_validate(response.json()["data"])

    async def _iter_file(self, filepath: str, chunk_size: int = 1024 * 1024):
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    async def upload(
        self,
        filepath: str,
        iter_content: AsyncIterable[bytes],
        overwrite: bool = False,
    ) -> bool:
        headers = {
            "file-path": urllib.parse.quote(filepath, safe='/'),
            "overwrite": "true" if overwrite else "false",
        }
        response = await self._request(
            "PUT",
            "/api/fs/put",
            headers=headers,
            content=iter_content,
        )
        return response.json()["code"] == 200

    async def mkdir(self, path: str) -> bool:
        response = await self._request("POST", "/api/fs/mkdir", json={"path": path})
        return response.json()["code"] == 200

    async def remove(self, path: str, names: List[str]) -> bool:
        response = await self._request(
            "POST",
            "/api/fs/remove",
            json={"dir": path, "names": names},
        )
        return response.json()["code"] == 200

    async def download(self, sign: str, filepath: str) -> AsyncIterable[bytes]:
        url = f"{self.host}/d{filepath}?sign={sign}"
        async with self.client.stream("GET", url, follow_redirects=True) as response:
            async for chunk in response.aiter_bytes():
                yield chunk
