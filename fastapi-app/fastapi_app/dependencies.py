from typing import Any, AsyncGenerator

from fastapi import Request
from psycopg import AsyncCursor, Rollback
from psycopg_pool import AsyncConnectionPool
from taskiq import TaskiqDepends


async def get_cursor(
    request: Request = TaskiqDepends(),
) -> AsyncGenerator[AsyncCursor[Any], None]:
    pool: AsyncConnectionPool = request.app.state.pg_pool

    async with pool.connection() as conn:
        async with conn.cursor(binary=True) as cur:
            yield cur


async def get_trans_cursor(
    request: Request = TaskiqDepends(),
) -> AsyncGenerator[AsyncCursor[Any], None]:
    pool: AsyncConnectionPool = request.app.state.pg_pool

    async with pool.connection() as conn:
        async with conn.cursor(binary=True) as cur:
            async with conn.transaction() as trans:
                try:
                    yield cur
                except Exception:
                    # If exception happens, we rollback.
                    raise Rollback(trans)
