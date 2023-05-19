import asyncio
from typing import AsyncGenerator, Awaitable, Callable, Union

import psycopg
import pytest
from aiohttp import web
from aiohttp.test_utils import BaseTestServer, TestClient, TestServer
from taskiq_aiohttp import populate_context

from aiohttp_app.__main__ import get_app
from aiohttp_app.settings import settings
from aiohttp_app.tkq import broker

ClientGenerator = Callable[
    [Union[BaseTestServer, web.Application]],
    Awaitable[TestClient],
]

URLResolver = Callable[[str], web.AbstractResource]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Anyio backend.

    Backend for anyio pytest plugin.
    :return: backend name.
    """
    return "asyncio"


@pytest.fixture
async def app() -> web.Application:
    """Test application."""
    return await get_app()


@pytest.fixture(autouse=True)
async def db_cleaner(app: web.Application) -> AsyncGenerator[None, None]:
    """Fixture used to clean database after tests."""
    yield

    # Cleans database after test is complete.
    async with await psycopg.AsyncConnection.connect(settings.postgres_url) as conn:
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE TABLE my_objs")


@pytest.fixture
async def test_client(
    app: web.Application,
) -> AsyncGenerator[TestClient, None]:
    """
    Create a test client.

    This function creates a TestServer
    and a test client for the application.

    Also this fixture populates context
    with needed variables.

    :param app: current application.
    :yield: ready to use client.
    """
    loop = asyncio.get_running_loop()
    server = TestServer(app)
    client = TestClient(server, loop=loop)

    await client.start_server()

    # This is important part.
    # Since InMemoryBroker doesn't
    # run in worker_process, we have to populate
    # broker's context by hand.
    populate_context(
        broker=broker,
        server=server.runner.server,
        app=app,
        loop=None,
    )

    yield client

    await client.close()
