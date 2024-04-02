import pytest
# from async_asgi_testclient import TestClient
from fastapi.testclient import TestClient


# pytestmark = pytest.mark.anyio


def test_get_words(client: TestClient):
    resp = client.get('/words')
    assert resp.status_code == 200
    assert resp.json() == []
    