from fastapi import Depends, HTTPException, status, APIRouter
import app.schemas as schemas
from app.database import get_db
from app.models import Item
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse
)
async def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    try:
        new_item = Item(**payload.dict())
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
    except IntegrityError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A item with the given details already exists.",
        ) from e
    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the item.",
        ) from e

    item_schema = schemas.ItemBaseSchema.from_orm(new_item)

    return schemas.ItemResponse(Status=schemas.Status.Success, Item=item_schema)


@router.get(
    "/{itemId}", status_code=status.HTTP_200_OK, response_model=schemas.GetItemResponse
)
async def get_item(itemId: int,  db: Session = Depends(get_db)):
    result = await db.execute(select(Item).filter(Item.id == itemId))
    item = result.scalars().first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Item with this id: `{itemId}` found",
        )

    try:
        return schemas.GetItemResponse(
            Status=schemas.Status.Success, User=schemas.ItemBaseSchema.model_validate(item)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user.",
        ) from e


@router.patch(
    "/{itemId}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.ItemResponse,
)
async def update_item(
    itemId: int, payload: schemas.ItemUpdate, db: Session = Depends(get_db)
):
    result = await db.execute(select(Item).filter(Item.id == itemId))
    item = result.scalars().first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Item with this id: `{itemId}` found",
        )

    try:
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(item, field, value)

        await db.commit()
        await db.refresh(item)
        item_schema = schemas.ItemBaseSchema.model_validate(item)
        return schemas.ItemResponse(Status=schemas.Status.Success, Item=item_schema)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A item with the given details already exists.",
        ) from e
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the item.",
        ) from e


@router.delete(
    "/{itemId}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DeleteItemResponse,
)
async def delete_item(itemId: int, db: Session = Depends(get_db)):
    try:
        result = await db.execute(select(Item).filter(Item.id == itemId))
        item = result.scalars().first()

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Item with this id: `{itemId}` found",
            )

        await db.delete(item)
        await db.commit()

        return schemas.DeleteItemResponse(
            Status=schemas.Status.Success, Message="Item deleted successfully"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the item.",
        ) from e


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.ListItemResponse
)
async def get_items(db: Session = Depends(get_db)):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return schemas.ListItemResponse(
        status=schemas.Status.Success, results=len(items), items=items
    )
