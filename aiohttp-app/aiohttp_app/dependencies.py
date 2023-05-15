from typing import Any, AsyncGenerator

from aiohttp import web
from aiohttp_deps import Depends
from psycopg import AsyncCursor, Rollback
from psycopg_pool import AsyncConnectionPool


async def get_cursor(
    app: web.Application = Depends(),
    row_factory: Any = None,
) -> AsyncGenerator[AsyncCursor[Any], None]:
    pool: AsyncConnectionPool = app["pg_pool"]

    async with pool.connection() as conn:
        async with conn.cursor(binary=True, row_factory=row_factory) as cur:
            yield cur


async def get_trans_cursor(
    app: web.Application = Depends(),
    row_factory: Any = None,
) -> AsyncGenerator[AsyncCursor[Any], None]:
    pool: AsyncConnectionPool = app["pg_pool"]

    async with pool.connection() as conn:
        async with conn.cursor(binary=True, row_factory=row_factory) as cur:
            async with conn.transaction() as trans:
                try:
                    yield cur
                except Exception:
                    # If exception happens, we rollback.
                    raise Rollback(trans)
