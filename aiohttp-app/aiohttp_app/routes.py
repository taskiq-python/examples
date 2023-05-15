from typing import Any

from aiohttp import web
from aiohttp_deps import Depends, Json, Query, Router
from psycopg import AsyncCursor
from psycopg.rows import DictRow, dict_row

from aiohttp_app.dependencies import get_cursor
from aiohttp_app.dtos import InputObjectDTO
from aiohttp_app.tasks import delayed_save

router = Router()


@router.get("/objects")
async def get_objects(
    # Here we pass row_factory arguement to the dependency,
    # so it automatically converts all rows to dicts.
    cursor: AsyncCursor[DictRow] = Depends(
        get_cursor, kwargs={"row_factory": dict_row}
    ),
    offset: int = Depends(Query(0)),
    limit: int = Depends(Query(10)),
) -> web.Response:
    result = await cursor.execute(
        "SELECT * FROM my_objs OFFSET %s LIMIT %s;",
        params=(offset, limit),
    )
    return web.json_response(await result.fetchall())


@router.put("/objects")
# Here we define our input_obj as a JSON dependency.
# Which means that we expect users to pass a JSON in body
# and we're going to validate it againts InputObjectDTO schema.
async def put_objects(input_obj: InputObjectDTO = Depends(Json())) -> web.Response:
    task = await delayed_save.kiq(input_obj)
    result = await task.wait_result()
    if result.return_value:
        return web.json_response({"state": "saved"})
    return web.json_response({"state": "conflict"})
