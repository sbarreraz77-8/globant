from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime as dt

class DepartmentBase(BaseModel):
    id: int
    department: Optional[str] = None

class DepartmentBatch(BaseModel):
    items: List[DepartmentBase] = Field(..., min_length=1, max_length=1000)

class JobBase(BaseModel):
    id: int
    job: Optional[str] = None

class JobBatch(BaseModel):
    items: List[JobBase] = Field(..., min_length=1, max_length=1000)

class HiredEmployeeBase(BaseModel):
    id: int
    name: Optional[str] = None
    datetime: Optional[dt] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None

class HiredEmployeeBatch(BaseModel):
    items: List[HiredEmployeeBase] = Field(..., min_length=1, max_length=1000)