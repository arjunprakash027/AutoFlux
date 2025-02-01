# Dockerfile to setup spark server
FROM openjdk:11

WORKDIR /app

ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark

# Install spark
RUN apt-get update && apt-get install -y curl unzip wget && rm -rf /var/lib/apt/lists/* && \
    curl -fsSl "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | tar -xz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark

ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

# Install delta lake
#RUN wget -o /opt/spark/jars/delta-core_2.12-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar

RUN mkdir -p ${SPARK_HOME}/conf && \
    echo "spark.jars.packages=io.delta:delta-core_2.12:2.4.0" >> $SPARK_HOME/conf/spark-defaults.conf

EXPOSE 4040 7077 8080 18080

CMD ["/bin/bash","-c","/opt/spark/sbin/start-master.sh && tail -f /dev/null"]

