from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Globant Data Engineering Challenge",
    description="API para migración y consulta de datos históricos",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT version();")).fetchone()
        return {"status": "success", "db_version": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))