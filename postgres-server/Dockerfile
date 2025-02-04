FROM postgres:latest

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=metastore

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk wget

RUN wget -O /usr/local/hive.tar.gz https://downloads.apache.org/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz && \
    tar -xzf /usr/local/hive.tar.gz -C /usr/local/ && \
    mv /usr/local/apache-hive-3.1.3-bin /usr/local/hive && \
    rm /usr/local/hive.tar.gz

ENV HIVE_HOME=/usr/local/hive
ENV PATH=$PATH:$HIVE_HOME/bin

RUN wget -q https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -P $HIVE_HOME/lib/

COPY hive-site.xml $HIVE_HOME/conf/hive-site.xml

COPY hive-schema.sql /docker-entrypoint-initdb.d/hive-schema.sql
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER postgres
EXPOSE 5432 9083

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]