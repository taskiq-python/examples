from datetime import datetime
from logging import getLogger
from typing import Any

from psycopg import AsyncCursor
from taskiq import TaskiqDepends

from fastapi_app.dependencies import get_trans_cursor
from fastapi_app.dtos import InputObjectDTO
from fastapi_app.tkq import broker


logger = getLogger(__name__)


@broker.task
async def delayed_save(
    target: InputObjectDTO,
    cursor: AsyncCursor[Any] = TaskiqDepends(get_trans_cursor),
) -> bool:
    logger.info("Saving object with name '%s'", target.name)
    await cursor.execute(
        "INSERT INTO my_objs(name) VALUES (%s)",
        params=(target.name,),
    )
    return True


@broker.task(schedule=[{"cron": "* * * * *"}])
async def scheduled_list(cursor: AsyncCursor[Any] = TaskiqDepends(get_trans_cursor)):
    cur = await cursor.execute(
        "SELECT COUNT(*) FROM my_objs",
    )
    count = await cur.fetchone()
    if count is not None:
        logger.info("Number of objects: %s", count[0])


@broker.task
async def dynamic_schedule(msg: str | None = None) -> None:
    logger.info("Func is executed at %s with message %s", datetime.now(), msg)
