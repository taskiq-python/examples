from typing import AsyncGenerator

from aiohttp import web
from psycopg_pool import AsyncConnectionPool

from aiohttp_app.settings import settings
from aiohttp_app.tkq import broker


async def setup_taskiq(_: web.Application) -> AsyncGenerator[None, None]:
    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()


async def setup_db(app: web.Application) -> AsyncGenerator[None, None]:
    pool = AsyncConnectionPool(settings.postgres_url)

    async with pool.connection() as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS my_objs(id SERIAL PRIMARY KEY, name TEXT)"
        )

    app["pg_pool"] = pool

    yield

    await pool.close()
