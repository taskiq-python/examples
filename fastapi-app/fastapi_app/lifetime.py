from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

from fastapi_app.settings import settings
from fastapi_app.tkq import broker


async def startup_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.startup()


async def shutdown_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.shutdown()


async def setup_db(app: FastAPI) -> None:
    app.state.pg_pool = AsyncConnectionPool(settings.postgres_url)
    await app.state.pg_pool.open()

    async with app.state.pg_pool.connection() as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS my_objs(id SERIAL PRIMARY KEY, name TEXT)"
        )


async def shutdown_db(app: FastAPI) -> None:
    await app.state.pg_pool.close()


def startup(app: FastAPI):
    async def _startup():
        await startup_taskiq()
        await setup_db(app)

    return _startup


def shutdown(app: FastAPI):
    async def _shutdown():
        await shutdown_taskiq()
        await shutdown_db(app)

    return _shutdown
