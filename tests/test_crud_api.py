import pytest
from httpx import AsyncClient
import json
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "OK!!"}

# @pytest.mark.asyncio
# async def test_create_item(client: AsyncClient):
#     test_request_payload = {"name": "something", "description": "something else"}

#     response = await client.post("/items", content=json.dumps(test_request_payload),)
#     print(response)

#     assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    response = await client.get("/items")
    print(response)

    assert response.status_code == 200


# def test_create_get_user(test_client, user_payload):
#     response = test_client.post("/api/users/", json=user_payload)
#     response_json = response.json()
#     assert response.status_code == 201

#     # Get the created user
#     response = test_client.get(f"/api/users/{user_payload['id']}")
#     assert response.status_code == 200
#     response_json = response.json()
#     assert response_json["Status"] == "Success"
#     assert response_json["User"]["id"] == user_payload["id"]
#     assert response_json["User"]["address"] == "123 Farmville"
#     assert response_json["User"]["first_name"] == "John"
#     assert response_json["User"]["last_name"] == "Doe"