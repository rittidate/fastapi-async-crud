from fastapi import FastAPI
from models import Base, Item # noqa
from database import engine, SessionLocal # noqa

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World2"}
