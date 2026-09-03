###  Purpose

The `app/` directory encapsulates all API application logic, request routing, data validation schemas, database models, and service layer implementations following clean architecture principles.

### Directory Structure
```
app/
├── api/
│   ├── __init__.py
│   ├── endpoints.py
│   └── metrics.py
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
├── services/
│   ├── __init__.py
│   └── ingestion_service.py
├── __init__.py
├── main.py
└── schemas.py
```
---

### 1. Presentation Layer (`app/api/`)
- `endpoints.py`: Exposes HTTP POST batch endpoints for departments, jobs, and employees. Validates incoming payload length (1 to 1000 items) and forwards parsing to the service layer.
- `metrics.py`: Exposes HTTP GET analytical endpoints:
  - `/metrics/hires-by-quarter`: Executes quarterly aggregations per department and job for 2021.
  - `/metrics/departments-above-average`: Executes Common Table Expression (CTE) query identifying departments exceeding the 2021 hiring mean.

---

### 2. Database Layer (`app/db/`)
- `database.py`: Establishes SQLAlchemy connection engine using connection pooling (`pool_pre_ping=True`) and provides the `get_db` dependency for contextual session lifecycles.
- `models.py`: Declarative SQLAlchemy ORM definitions for:
  - `Department`: Department entity representation.
  - `Job`: Job title entity representation.
  - `HiredEmployee`: Employee hiring transactions.
  - `LoadControl`: Audit logging for ingestion batches.
  - `LoadError`: Dead-letter storage for unprocessable records.

---

### 3. Business Logic Layer (`app/services/`)
- `ingestion_service.py`: Contains `process_batch()`.
  - Generates tracking rows in `load_control`.
  - Performs item-by-item schema compliance checks.
  - Segregates records with null values or invalid formats into `load_errors`.
  - Executes PostgreSQL-specific bulk insertions with `ON CONFLICT (id) DO NOTHING` for idempotency.
  - Records batch completion metrics and execution timestamps.

---

### 4. Schema Layer (`app/schemas.py`)
- Pydantic v2 schemas defining input models (`DepartmentBase`, `JobBase`, `HiredEmployeeBase`) and batch containers enforcing `min_length=1` and `max_length=1000`.

---

### 5. Application Entrypoint (`app/main.py`)
- Initializes the `FastAPI` application instance, mounts sub-routers with prefix `/api/v1`, and defines top-level health verification endpoints.

---
