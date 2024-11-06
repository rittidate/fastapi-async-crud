import app.schemas as schemas
import app.models as models
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session


router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse
)
async def create_item(payload: schemas.ItemCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        new_item = models.Item(**payload.dict())
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
    except IntegrityError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with the given details already exists.",
        ) from e
    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user.",
        ) from e

    item_schema = schemas.ItemBaseSchema.from_orm(new_item)

    return schemas.ItemResponse(Status=schemas.Status.Success, Item=item_schema)


@router.get(
    "/{itemId}", status_code=status.HTTP_200_OK, response_model=schemas.GetItemResponse
)
async def get_item(itemId: int,  db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(models.Item).filter(models.Item.id == itemId))
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
    itemId: int, payload: schemas.ItemUpdate, db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(select(models.Item).filter(models.Item.id == itemId))
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
async def delete_item(itemId: int, db: AsyncSession = Depends(get_db_session)):
    try:
        item_query = await db.execute(select(models.Item).where(models.Item.id == itemId))
        item = item_query.scalar_one()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Item with this id: `{itemId}` found",
            )
        await db.delete(item)
        await db.execute()
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
async def get_items(db: AsyncSession = Depends(get_db_session)):
    q = select(models.Item)
    result = await db.execute(q)
    items = result.scalars().all()
    return schemas.ListItemResponse(
        status=schemas.Status.Success, results=len(items), items=items
    )
