FROM python:latest

WORKDIR /app

COPY . ./

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    git \
    build-essential \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH"

RUN /root/.local/bin/poetry config virtualenvs.create false && \ 
    /root/.local/bin/poetry install --no-root && \
    rm -rf /root/.cache/pypoetry

CMD ["tail","-f","/dev/null"]

