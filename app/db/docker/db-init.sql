CREATE TABLE IF NOT EXISTS public_holidays (
    id SERIAL PRIMARY KEY,
    holiDate TEXT NOT NULL,
    holiName TEXT NOT NULL
)