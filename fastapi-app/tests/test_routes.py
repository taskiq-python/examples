import uuid

import pytest
from fastapi.testclient import TestClient
from starlette import status


@pytest.mark.anyio
async def test_obj_creation(client: TestClient) -> None:
    name = uuid.uuid4().hex
    response = client.put(
        "/objects",
        json={"name": name},
    )
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/objects").json()
    assert len(response) == 1
    assert response[0]["name"] == name
