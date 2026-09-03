from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Sequence
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class LoadControl(Base):
    __tablename__ = "load_control"
    id = Column(Integer, primary_key=True, index=True)
    target_table = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_records = Column(Integer, default=0)
    success_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)

class LoadError(Base):
    __tablename__ = "load_errors"
    id = Column(Integer, primary_key=True, index=True)
    load_control_id = Column(Integer, ForeignKey("load_control.id"), nullable=False)
    raw_data = Column(Text, nullable=False)
    error_message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(255), nullable=False)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String(255), nullable=False)

class HiredEmployee(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)