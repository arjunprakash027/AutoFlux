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
    delta-spark==2.2.0

# Configure dbt
RUN mkdir -p /root/.dbt && \
    mkdir -p /home/dbt_user/dbt_packages && \
    chmod -R 755 /home/dbt_user

COPY profiles.yml /root/.dbt/profiles.yml
COPY . .

# Validation step to check environment
RUN python -c "import pyspark, dbt"
RUN dbt --version

ENTRYPOINT ["./entrypoint.sh"]

