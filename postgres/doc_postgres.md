### Purpose
The `postgres/` directory contains Data Definition Language (DDL) specifications and schema management scripts corresponding to the production database objects.

---

### Directory Structure
```
postgres/
└── globant/
    └── public/
        ├── tables/
        │   ├── departments.sql
        │   ├── hired_employees.sql
        │   ├── jobs.sql
        │   ├── load_control.sql
        │   └── load_errors.sql
        ├── views/
        └── functions/
```

---

### Live Database Access (Read-Only)
The Serverless PostgreSQL database is hosted on Neon.tech. Reviewers can connect using any standard SQL client (DBeaver, DataGrip, pgAdmin) to inspect the ingested raw data, schemas, and audit tables. 

**Connection String (Read-Only Role):**
`postgresql://revisor_globant:prueba_tecnica@ep-lingering-moon-ayh7w3lg-pooler.c-5.us-east-2.aws.neon.tech/globant?sslmode=require&channel_binding=require`