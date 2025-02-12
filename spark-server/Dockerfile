# spark/Dockerfile
FROM openjdk:11-jdk-slim

ARG SPARK_VERSION=3.3.2
ARG DELTA_VERSION=2.2.0

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    python3 \
    procps \
    curl \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Download and install Spark
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && tar xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop3 /spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

RUN wget -q https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -P /spark/jars/
COPY hive-site.xml /spark/conf/

# Add Delta Lake JARs
RUN curl -fL --retry 3 --retry-delay 5 \
    -o /spark/jars/delta-core_2.12-${DELTA_VERSION}.jar \
    https://repo.maven.apache.org/maven2/io/delta/delta-core_2.12/${DELTA_VERSION}/delta-core_2.12-${DELTA_VERSION}.jar && \
    curl -fL --retry 3 --retry-delay 5 \
    -o /spark/jars/delta-storage-${DELTA_VERSION}.jar \
    https://repo.maven.apache.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar

# Configure Spark
COPY entrypoint_master.sh entrypoint_worker.sh /
RUN chmod +x /entrypoint_master.sh /entrypoint_worker.sh

ENV SPARK_HOME=/spark
ENV PATH=$PATH:$SPARK_HOME/bin

RUN ln -s /usr/bin/python3 /usr/local/bin/python

EXPOSE 7077 8080 10000
