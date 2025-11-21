import os

import pytest

from beetle.client import OpenListClient


@pytest.fixture
def client():
    env_keys = ["OPENLIST_HOST", "OPENLIST_TOKEN"]
    vars = [var for var in env_keys if not os.getenv(var)]
    if vars:
        pytest.skip(f"Missing required environment variables: {', '.join(vars)}")
    return OpenListClient(
        host=os.getenv("OPENLIST_HOST"),
        token=os.getenv("OPENLIST_TOKEN"),
    )


@pytest.mark.asyncio
async def test_list(client: OpenListClient):
    await client.list("/")


@pytest.mark.asyncio
async def test_mkdir(client: OpenListClient):
    path = "/local/test/a/b"
    result = await client.mkdir(path)
    assert result


@pytest.mark.asyncio
async def test_upload(client: OpenListClient):
    filepath = "/local/test/a/b/test_sdk.py"

    async def _iter():
        yield b"123"

    result = await client.upload(filepath, _iter())
    assert result


@pytest.mark.asyncio
async def test_download(client: OpenListClient):
    path = "/local/test/a/b"
    response = await client.list(path)
    for item in response.content:
        print(item)
        async for chunk in client.download(item.sign, "/local/test/a/b/test_sdk.py"):
            print(chunk)


@pytest.mark.asyncio
async def test_remove(client: OpenListClient):
    path = "/local"
    result = await client.remove(path, ["test"])
    assert result


@pytest.mark.asyncio
async def test_cleanup(client: OpenListClient):
    src_path = "/local/"
    filepath = "/local/test/a/b/test_sdk.py"
    src_path = src_path.rstrip("/")
    remove = [os.path.split(filepath)]

    await test_upload(client)
    while remove:
        path, name = remove.pop()
        await client.remove(path, names=[name])
        response = await client.list(path, refresh=True)

        if len(response.content) == 0 and src_path:
            parent_path, name = os.path.split(path)
            if name and parent_path.startswith(src_path):
                remove.append((parent_path, name))

    print("ok")
