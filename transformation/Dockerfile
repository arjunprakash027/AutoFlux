FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    netcat-openbsd \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip wheel && \
    pip install \
    numpy==1.24.4 \
    pandas==1.5.3 \
    dbt-duckdb==1.9.2 \
    'ibis-framework[duckdb]' \
    # Kaggle is needed for ingestion in this project
    kaggle

# Configure dbt
RUN mkdir -p /root/.dbt && \
    mkdir -p /home/dbt_user/dbt_packages && \
    chmod -R 755 /home/dbt_user

COPY profiles.yml /root/.dbt/profiles.yml

# Only if you are using kaggle for ingestion from kaggle repository
COPY kaggle.json /root/.config/kaggle/kaggle.json

RUN chmod 600 /root/.config/kaggle/kaggle.json

COPY . .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

