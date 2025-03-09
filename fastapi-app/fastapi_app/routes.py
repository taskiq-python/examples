import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from psycopg import AsyncCursor

from fastapi_app.dependencies import get_cursor
from fastapi_app.dtos import InputObjectDTO, InputScheduleDTO, OutputObjectDTO
from fastapi_app import tasks
from fastapi_app.tkq_sched import redis_source

router = APIRouter()


@router.get("/objects", response_model=List[OutputObjectDTO])
async def get_objects(
    # Here we pass row_factory arguement to the dependency,
    # so it automatically converts all rows to dicts.
    cursor: AsyncCursor[Any] = Depends(get_cursor),
    offset: int = 0,
    limit: int = 10,
) -> list[OutputObjectDTO]:
    result = await cursor.execute(
        "SELECT id, name FROM my_objs OFFSET %s LIMIT %s;",
        params=(offset, limit),
    )

    return [OutputObjectDTO(id=id, name=name) for id, name in await result.fetchall()]


@router.put("/objects")
async def put_objects(input_obj: InputObjectDTO) -> Dict[str, str]:
    print("Sending delayed save")
    task = await tasks.delayed_save.kiq(input_obj)
    print("Task sent")
    result = await task.wait_result()
    print("Got task result")
    if result.return_value:
        return {"state": "saved"}
    return {"state": "conflict"}


@router.post("/schedule")
async def schedule_task(dto: InputScheduleDTO) -> None:
    target_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=dto.delay,
    )
    print("Task is scheduled at", target_time)
    await tasks.dynamic_schedule.schedule_by_time(
        source=redis_source,
        time=target_time,
        msg=dto.message,
    )
