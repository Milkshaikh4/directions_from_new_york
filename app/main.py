from fastapi import FastAPI
from app.routes.items import router as items_router
from app.database import connect_to_mongo

connect_to_mongo()

app = FastAPI()

app.include_router(items_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Backend Challenge API"}
