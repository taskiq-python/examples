from http import HTTPStatus

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient


@pytest.mark.anyio
async def test_health(test_client: TestClient):
    """Test that healthcheck is working."""
    put_resp = await test_client.put("/objects", json={"name": "pupa"})
    assert put_resp.status == HTTPStatus.OK
    response = await test_client.get("/objects")
    assert response.status == HTTPStatus.OK
    rjson = await response.json()
    assert len(rjson) == 1
    obj = rjson[0]
    assert "id" in obj
    assert obj["name"] == "pupa"
