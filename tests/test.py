
import aiohttp
import pytest_asyncio

from contextlib import ExitStack


import pytest
from async_asgi_testclient import TestClient


# pytestmark = pytest.mark.anyio


@pytest.mark.asyncio
async def test_get_words(client: TestClient):
    resp = await client.get('/')
    assert resp.status_code == 404
    assert resp.json() == {"detail":"Not Found"}
    