-- Add migration scripts here.
CREATE DATABASE platable;

CREATE USER ${POSTGRES_USER} WITH PASSWORD ${POSTGRES_PASSWORD};
GRANT ALL PRIVILEGES ON DATABASE platable TO ${POSTGRES_USER};