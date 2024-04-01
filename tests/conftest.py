from contextlib import ExitStack

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from src.main import init_app

# pytestmark = pytest.mark.anyio

@pytest_asyncio.fixture(scope="session")
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest_asyncio.fixture(scope="function")
async def client(app):
    host, port = "127.0.0.1", "8000"
    scope = {"client": (host, port)}

    async with TestClient(
        app, scope=scope, headers={"X-User-Fingerprint": "Test"}
    ) as client:
        yield client