from typing import Any

from aiohttp_deps import Depends
from psycopg import AsyncCursor

from aiohttp_app.dependencies import get_trans_cursor
from aiohttp_app.dtos import InputObjectDTO
from aiohttp_app.tkq import broker


@broker.task
async def delayed_save(
    target: InputObjectDTO,
    cursor: AsyncCursor[Any] = Depends(get_trans_cursor),
) -> bool:
    await cursor.execute(
        "INSERT INTO my_objs(name) VALUES (%s)",
        params=(target.name,),
    )
    return True
