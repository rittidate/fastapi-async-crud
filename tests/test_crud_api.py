import pytest
import json
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "OK!!"}


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    test_request_payload = {"name": "something", "description": "something else"}

    response = await client.post("/items/", content=json.dumps(test_request_payload),)
    print(response)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    response = await client.get("/items/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient, not_found_item_id):
    response = await client.get(f"/items/{not_found_item_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No Item with this id: `{not_found_item_id}` found"
