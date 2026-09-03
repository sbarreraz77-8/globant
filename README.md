
### Overview
This repository delivers an end-to-end data engineering solution designed to load records and serve analytical metrics via a high-performance REST API. The system handles data ingestion from CSV files, implements strict schema validation and batching, isolates malformed rows into audit tables, ensures idempotency, and delivers business metrics through dedicated SQL-backed endpoints.

The architecture is containerized with Docker, continuously deployed to Google Cloud Platform (Cloud Run) via GitHub Actions, and backed by a Serverless PostgreSQL database.

---

### Interactive API Documentation (Swagger UI)
The API includes an auto-generated, interactive interface to explore endpoints, validate payload schemas, and execute test requests directly from your browser. 

**Access the Swagger UI here:** [https://globant-api-340695378961.us-central1.run.app/docs](https://globant-api-340695378961.us-central1.run.app/docs)

---

### Architectural Characteristics
- **Layered Decoupling:** Complete separation of presentation (FastAPI routes), data validation (Pydantic), business logic (Services), and persistence (SQLAlchemy / PostgreSQL).
- **Batch Processing & Isolation:** The ingestion pipeline accepts payloads of 1 to 1,000 records per transaction. Records with missing attributes or validation faults are separated into a dead-letter table (`load_errors`) without aborting valid inserts.
- **Idempotency:** Native PostgreSQL upsert behavior prevents duplicate primary key collisions and guarantees consistent database state across identical payload replays.
- **Observability:** Telemetry on incoming batches (start/end timestamp, total rows, successful inserts, failed count) is persisted in `load_control`.
- **Serverless Cloud Deployment:** The application runs on Google Cloud Run with automatic scaling to zero when idle, consuming minimal resource quotas within Google Cloud Free Tier.

---

### Directory Documentation Index

Detailed documentation for each sub-folder component is maintained in module-specific markdown files:

| Module / Directory | Documentation Path | Description |
| :--- | :--- | :--- |
| **CI/CD** | [`cicd`](.github/doc_cicd.md) | GitHub Actions CI/CD pipeline, GCP authentication, Artifact Registry, and deployment. |
| **App Source** | [`app.md`](app/doc_app.md) | API routing, data models, Pydantic schemas, and ingestion services. |
| **Datasets** | [`data.md`](data/doc_data.md) | Data |
| **Database DDL** | [`postgres.md`](postgres/doc_postgres.md) | Relational schema definitions, constraints, indices, and audit tables. |
| **Script Test** | [`scripts.md`](scripts/doc_scripts.md) | Automated chunked CSV loaders and SQL metrics testing scripts. |

---

### API Endpoints Reference

#### Ingestion Endpoints (Batch 1-1000 Rows)
- `POST /api/v1/departments/batch` - Ingests department records.
- `POST /api/v1/jobs/batch` - Ingests job titles and identifiers.
- `POST /api/v1/employees/batch` - Ingests employee hiring records, routing invalid rows to `load_errors`.

#### Analytical Metrics Endpoints
- `GET /api/v1/metrics/hires-by-quarter` - Aggregates employee hires by department and job across each quarter of 2021, ordered alphabetically.
- `GET /api/v1/metrics/departments-above-average` - Lists departments hiring more employees than the annual mean across all departments in 2021, ranked descending.

---

### Local Development & Execution

- Conda
- PostgreSQL instance connection string

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --env-file .env
python scripts/load_csv.py
python scripts/test_metrics.py
```
