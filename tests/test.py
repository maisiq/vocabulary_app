import pytest
from async_asgi_testclient import TestClient
# from fastapi.testclient import TestClient


# pytestmark = pytest.mark.anyio


@pytest.fixture
def word_data():
    return {
        'word': 'string',
        'transcription': 'string'
    }

async def test_get_home(client: TestClient):
    resp = await client.get('/')
    assert resp.status_code == 404
    # assert resp.json() == []

async def test_get_words(client: TestClient):
    resp = await client.get('/words')
    # assert True
    assert resp.status_code == 200
    assert resp.json() == []


async def test_can_create_word(client: TestClient, word_data: dict):

    resp = await client.post('/words', json=word_data)
    
    assert resp.status_code == 201


async def test_can_create_and_retrieve_the_word(client: TestClient, word_data: dict):
    await client.post('/words', json=word_data)

    resp = await client.get(f"/words/{word_data.get('word')}")

    assert resp.status_code == 200


async def test_cant_create_same_word_twice(client: TestClient, word_data: dict):
    await client.post('/words', json=word_data)

    resp = await client.post('/words', json=word_data)

    assert resp.status_code == 400
