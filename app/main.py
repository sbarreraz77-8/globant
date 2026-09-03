from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Globant",
    description="Assesment",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")