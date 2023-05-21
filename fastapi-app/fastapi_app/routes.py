from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Response
from psycopg import AsyncCursor

from fastapi_app.dependencies import get_cursor
from fastapi_app.dtos import InputObjectDTO, OutputObjectDTO
from fastapi_app.tasks import delayed_save

router = APIRouter()


@router.get("/objects", response_model=List[OutputObjectDTO])
async def get_objects(
    # Here we pass row_factory arguement to the dependency,
    # so it automatically converts all rows to dicts.
    cursor: AsyncCursor[Any] = Depends(get_cursor),
    offset: int = 0,
    limit: int = 10,
) -> Response:
    result = await cursor.execute(
        "SELECT id, name FROM my_objs OFFSET %s LIMIT %s;",
        params=(offset, limit),
    )

    return [OutputObjectDTO(id=id, name=name) for id, name in await result.fetchall()]


@router.put("/objects")
async def put_objects(input_obj: InputObjectDTO) -> Dict[str, str]:
    print("SENDING")
    task = await delayed_save.kiq(input_obj)
    print("SENT")
    result = await task.wait_result()
    print("RESULT GOT")
    if result.return_value:
        return {"state": "saved"}
    return {"state": "conflict"}
