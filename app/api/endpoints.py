from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io

from app.db.database import get_db
from app.db.models import Department, Job, HiredEmployee
from app.schemas import DepartmentBatch, JobBatch, HiredEmployeeBatch, DepartmentBase, JobBase, HiredEmployeeBase
from app.services.ingestion_service import process_batch
from app.api.metrics import router as metrics_router

router = APIRouter()
router.include_router(metrics_router)

@router.post("/departments/batch")
def upload_departments_batch(payload: DepartmentBatch, db: Session = Depends(get_db)):
    result = process_batch(
        db=db,
        target_table_name="departments",
        model_class=Department,
        batch_data=[item.model_dump() for item in payload.items],
        pydantic_schema=DepartmentBase
    )
    return result

@router.post("/jobs/batch")
def upload_jobs_batch(payload: JobBatch, db: Session = Depends(get_db)):
    result = process_batch(
        db=db,
        target_table_name="jobs",
        model_class=Job,
        batch_data=[item.model_dump() for item in payload.items],
        pydantic_schema=JobBase
    )
    return result

@router.post("/employees/batch")
def upload_employees_batch(payload: HiredEmployeeBatch, db: Session = Depends(get_db)):
    result = process_batch(
        db=db,
        target_table_name="hired_employees",
        model_class=HiredEmployee,
        batch_data=[item.model_dump() for item in payload.items],
        pydantic_schema=HiredEmployeeBase
    )
    return result