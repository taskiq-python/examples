from typing import Any, AsyncGenerator, Generator

import psycopg
import pytest
import taskiq_fastapi
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from fastapi_app.__main__ import get_app
from fastapi_app.settings import settings
from fastapi_app.tkq import broker


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def db_cleaner() -> AsyncGenerator[None, None]:
    """Fixture used to clean database after tests."""

    yield

    # Cleans database after test is complete.
    async with await psycopg.AsyncConnection.connect(settings.postgres_url) as conn:
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE TABLE my_objs")


@pytest.fixture
def fastapi_app() -> FastAPI:
    app = get_app()

    return app


@pytest.fixture(autouse=True)
def init_taskiq_deps(fastapi_app: FastAPI):
    # This is important part. Here we add dependency context,
    # this thing helps in resolving dependencies for tasks
    # for inmemory broker.
    taskiq_fastapi.populate_dependency_context(broker, fastapi_app)

    yield

    broker.custom_dependency_context = {}


@pytest.fixture
def client(fastapi_app: FastAPI) -> Generator[TestClient, None, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    with TestClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
