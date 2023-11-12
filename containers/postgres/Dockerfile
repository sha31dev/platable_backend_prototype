FROM postgres:13

ADD migrations /docker-entrypoint-initdb.d/

RUN sed -i 's/${POSTGRES_USER}/'"$POSTGRES_USER"'/' /docker-entrypoint-initdb.d/*.sql && \
    sed -i 's/${POSTGRES_PASSWORD}/'"$POSTGRES_PASSWORD"'/' /docker-entrypoint-initdb.d/*.sql && \
    sed -i 's/${POSTGRES_DB}/'"$POSTGRES_DB"'/' /docker-entrypoint-initdb.d/*.sql
