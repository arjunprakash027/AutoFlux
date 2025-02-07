FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=metastore

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk wget

RUN wget -O /usr/local/hadoop.tar.gz https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz && \
    tar -xzf /usr/local/hadoop.tar.gz -C /usr/local/ && \
    mv /usr/local/hadoop-3.4.1 /usr/local/hadoop && \
    rm /usr/local/hadoop.tar.gz

RUN wget -O /usr/local/hive.tar.gz https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz && \
    tar -xzf /usr/local/hive.tar.gz -C /usr/local/ && \
    mv /usr/local/apache-hive-3.1.3-bin /usr/local/hive && \
    rm /usr/local/hive.tar.gz

ENV HIVE_HOME=/usr/local/hive
ENV HADOOP_HOME=/usr/local/hadoop
#ENV HADOOP_PREFIX=$HADOOP_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${HADOOP_HOME}/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin:${JAVA_HOME}/bin:${PATH}"

RUN wget -q https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -P $HIVE_HOME/lib/

COPY hive-site.xml $HIVE_HOME/conf/hive-site.xml

COPY hive-schema.sql /docker-entrypoint-initdb.d/hive-schema.sql
COPY entrypoint.sh /entrypoint.sh

# RUN mkdir -p /spark-warehouse && \
#     chmod -R 777 /spark-warehouse 
RUN chmod +x /entrypoint.sh

EXPOSE 5432 9083

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]