FROM postgres:latest

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=metastore

USER postgres

COPY hive-schema.sql /docker-entrypoint-initdb.d/hive-schema.sql

RUN chmod 644 /docker-entrypoint-initdb.d/hive-schema.sql

EXPOSE 5432

CMD ["postgres"]

