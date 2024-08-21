from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users, auth

# for reloading database. but i prefer using alembic for backwards compatibility. so lets comment this out
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Swift Send API!"}
