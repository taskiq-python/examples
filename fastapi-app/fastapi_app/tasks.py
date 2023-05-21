from typing import Any

from psycopg import AsyncCursor
from taskiq import TaskiqDepends

from fastapi_app.dependencies import get_trans_cursor
from fastapi_app.dtos import InputObjectDTO
from fastapi_app.tkq import broker


@broker.task
async def delayed_save(
    target: InputObjectDTO,
    cursor: AsyncCursor[Any] = TaskiqDepends(get_trans_cursor),
) -> bool:
    await cursor.execute(
        "INSERT INTO my_objs(name) VALUES (%s)",
        params=(target.name,),
    )
    return True
