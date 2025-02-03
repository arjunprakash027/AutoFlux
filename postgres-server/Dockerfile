FROM postgres:latest

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=metastore

COPY hive-schema.sql /docker-entrypoint-initdb.d/hive-schema.sql
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER postgres
EXPOSE 5432

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]