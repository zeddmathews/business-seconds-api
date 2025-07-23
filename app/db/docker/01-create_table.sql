CREATE TABLE IF NOT EXISTS public_holidays (
    id SERIAL PRIMARY KEY,
    holi_date DATE NOT NULL UNIQUE,
    observed_date DATE NOT NULL,
    holi_name TEXT NOT NULL,
    day_of_week TEXT NOT NULL
);