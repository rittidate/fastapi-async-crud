from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import item
from app.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(item.router, tags=["Items"], prefix="/items")


@app.get("/health")
async def root():
    return {"message": "OK!!"}
