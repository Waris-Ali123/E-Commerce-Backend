from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}