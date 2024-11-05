from fastapi import FastAPI
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def root():
    return {"message": "OK!!"}
