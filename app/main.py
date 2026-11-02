from collections.abc import AsyncIterator

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers.auth_router import router as auth_router

app=FastAPI(title="Tender and Quotation Assessment System")

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Tender Assessment API is running"}


