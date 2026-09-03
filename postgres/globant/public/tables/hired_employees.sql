CREATE TABLE public.hired_employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    department_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    CONSTRAINT fk_department FOREIGN KEY(department_id) REFERENCES public.departments(id),
    CONSTRAINT fk_job FOREIGN KEY(job_id) REFERENCES public.jobs(id)
);