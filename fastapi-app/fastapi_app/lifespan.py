from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

from fastapi_app.settings import settings
from fastapi_app.tkq import broker


async def setup_db(app: FastAPI) -> None:
    app.state.pg_pool = AsyncConnectionPool(settings.postgres_url, open=False)
    await app.state.pg_pool.open()

    async with app.state.pg_pool.connection() as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS my_objs(id SERIAL PRIMARY KEY, name TEXT)"
        )


async def shutdown_db(app: FastAPI) -> None:
    await app.state.pg_pool.close()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await setup_db(app)
    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()
    await shutdown_db(app)
