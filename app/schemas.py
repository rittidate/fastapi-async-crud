from enum import Enum
from pydantic import BaseModel
from typing import List


class ItemSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

class ItemCreate(BaseModel):
    name: str
    description: str

class ItemUpdate(BaseModel):
    name: str
    description: str | None = None

class Status(Enum):
    Success = "Success"
    Failed = "Failed"


class ItemResponse(BaseModel):
    Status: Status
    Item: ItemSchema

class ItemResponseSuccess(BaseModel):
    Status: Status


class DeleteItemResponse(BaseModel):
    Status: Status
    Message: str

class ListItemResponse(BaseModel):
    status: Status
    results: int
    items: List[ItemSchema]