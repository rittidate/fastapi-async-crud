import pytest
import json
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "OK!!"}


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, item_payload):
    response = await client.post("/items/", content=json.dumps(item_payload),)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_update_item(client: AsyncClient, item_payload):
    response = await client.post("/items/", json=item_payload)
    response_json = response.json()
    assert response.status_code == 201

    item_update_payload = {"name": "item Update 1"}
    response = await client.patch(
        f"/items/{item_payload['id']}", json=item_update_payload
    )
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["Item"]["id"] == item_payload["id"]
    assert response_json["Item"]["name"] == "item Update 1"
    assert response_json["Item"]["description"] == "item description"


@pytest.mark.asyncio
async def test_create_delete_item(client: AsyncClient, item_payload):
    response = await client.post("/items/", json=item_payload)
    response_json = response.json()
    assert response.status_code == 201

    # Delete the created item
    response = await client.delete(f"/items/{item_payload['id']}")
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["Message"] == "Item deleted successfully"

    # Get the deleted item
    response = await client.get(f"/items/{item_payload['id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No Item with this id: `{item_payload['id']}` found"


@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    response = await client.get("/items/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient, not_found_item_id):
    response = await client.get(f"/items/{not_found_item_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No Item with this id: `{not_found_item_id}` found"


@pytest.mark.asyncio
async def test_create_item_wrong_payload(client: AsyncClient):
    response = await client.post("/items/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_item_wrong_payload(client: AsyncClient, item_payload):
    response = await client.post("/items/", json=item_payload)
    assert response.status_code == 201

    item_update_payload = {"name": 1}

    response = await client.patch(f"/items/{item_payload['id']}", json=item_update_payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_item_doesnt_exist(client: AsyncClient):
    item_id = 200
    item_update_payload = {"name": "item Update 1"}

    response = await client.patch(f"/items/{item_id}", json=item_update_payload)
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No Item with this id: `{item_id}` found"
