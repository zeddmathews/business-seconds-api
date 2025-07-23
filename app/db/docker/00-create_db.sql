SELECT 'CREATE DATABASE recomed'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'recomed')\gexec