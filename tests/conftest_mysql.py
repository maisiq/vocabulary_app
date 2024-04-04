import asyncio
from contextlib import ExitStack
import os

import pytest
from pytest_mysql import factories
from sqlalchemy import text
from async_asgi_testclient import TestClient

from src.main import init_app
from src.config.db_config import sessionmanager, get_session, TestDbConfig


# pytestmark = pytest.mark.anyio


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
async def client(app):
    async with TestClient(app) as client:
        yield client


# default event_loop fixture is function scope
@pytest.fixture(scope="session")
def event_loop(request):
    try:
        # set new policy if OS == Windows else pass
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


test_db = factories.mysql_noproc(port=3306, user='root', host='localhost')


@pytest.fixture(scope="function", autouse=True)
async def connection_test(test_db, event_loop):
    connection_str = os.environ.get('MYSQLDB_URI', None)

    sessionmanager.init(connection_str)
    yield
    await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(autouse=True)
async def session_override(app, connection_test):
    async def get_session_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override