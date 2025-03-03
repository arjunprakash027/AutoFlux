FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    netcat-openbsd \
    openjdk-17-jdk \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Java home properly (persistent environment variables)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYSPARK_PYTHON=/usr/local/bin/python
ENV PYSPARK_DRIVER_PYTHON=/usr/local/bin/python

# Install Python dependencies
RUN pip install --upgrade pip wheel && \
    pip install \
    pyspark==3.3.2 \
    dbt-spark[PyHive] \
    delta-spark==2.2.0 \
    numpy==1.24.4 \
    pandas==1.5.3 \
    # Kaggle is needed for ingestion in this project
    kaggle

# Configure dbt
RUN mkdir -p /root/.dbt && \
    mkdir -p /home/dbt_user/dbt_packages && \
    chmod -R 755 /home/dbt_user

COPY profiles.yml /root/.dbt/profiles.yml

# Only ig you are using kaggle for ingestion from kaggle repository
COPY kaggle.json /root/.config/kaggle/kaggle.json

RUN chmod 600 /root/.config/kaggle/kaggle.json

COPY . .

ENTRYPOINT ["./entrypoint.sh"]

