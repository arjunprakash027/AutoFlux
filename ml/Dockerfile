FROM python:3.11-slim

WORKDIR /app

COPY . ./

# java development kit is neccessary for pyspark to run
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    git \
    build-essential \
    openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false && \ 
    poetry install --no-root && \
    rm -rf /root/.cache/pypoetry

RUN python install_spark_dependencies.py

EXPOSE 6969

ENTRYPOINT [ "./start_server.sh" ]

