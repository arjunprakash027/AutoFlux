FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \ 
    pip install dbt-postgres psycopg2-binary

RUN mkdir -p /root/.dbt
RUN mkdir -p /home/dbt_user/dbt_packages && chmod -R 755 /home/dbt_user/dbt_packages

COPY profiles.yml /root/.dbt/profiles.yml
COPY . ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
#CMD ["tail","-f","/dev/null"]

