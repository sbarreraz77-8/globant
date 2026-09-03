CREATE TABLE public.load_errors (
    id SERIAL PRIMARY KEY,
    load_control_id INTEGER NOT NULL,
    raw_data TEXT NOT NULL,
    error_message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_load_control FOREIGN KEY(load_control_id) REFERENCES public.load_control(id)
);