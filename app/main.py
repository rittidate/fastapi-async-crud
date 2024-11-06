from fastapi import FastAPI

from app import item


app = FastAPI()


app.include_router(item.router, tags=["Items"], prefix="/items")


@app.get("/health")
async def health():
    return {"message": "OK!!"}
