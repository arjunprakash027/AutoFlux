FROM python:3.11-slim

WORKDIR /app

COPY . ./

# java development kit is neccessary for pyspark to run
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    git \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-root && \
    rm -rf /root/.cache/pypoetry

EXPOSE 6969

RUN chmod +x /app/start_server.sh

ENTRYPOINT [ "/bin/bash","/app/start_server.sh" ]

