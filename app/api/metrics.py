from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/hires-by-quarter")
def get_hires_by_quarter(db: Session = Depends(get_db)):

    query = text("""
        SELECT 
            d.department,
            j.job,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 END) AS q1,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 END) AS q2,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 END) AS q3,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 END) AS q4
        FROM hired_employees e
        INNER JOIN departments d ON e.department_id = d.id
        INNER JOIN jobs j ON e.job_id = j.id
        WHERE EXTRACT(YEAR FROM e.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department ASC, j.job ASC;
    """)
    
    result = db.execute(query).fetchall()
    
    return [
        {
            "department": row.department,
            "job": row.job,
            "Q1": row.q1,
            "Q2": row.q2,
            "Q3": row.q3,
            "Q4": row.q4
        }
        for row in result
    ]

@router.get("/departments-above-average")
def get_departments_above_average(db: Session = Depends(get_db)):

    query = text("""
        WITH dept_hires AS (
            SELECT 
                d.id,
                d.department,
                COUNT(e.id) AS hired
            FROM departments d
            INNER JOIN hired_employees e ON d.id = e.department_id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.id, d.department
        ),
        average_hires AS (
            SELECT AVG(hired) AS avg_hired FROM dept_hires
        )
        SELECT 
            dh.id,
            dh.department,
            dh.hired
        FROM dept_hires dh, average_hires ah
        WHERE dh.hired > ah.avg_hired
        ORDER BY dh.hired DESC;
    """)
    
    result = db.execute(query).fetchall()
    
    return [
        {
            "id": row.id,
            "department": row.department,
            "hired": row.hired
        }
        for row in result
    ]