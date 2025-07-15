FROM python:3.13-slim-bullseye AS requirements-stage

WORKDIR /tmp

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN pip install uv
COPY ./pyproject.toml ./uv.lock* /tmp/
RUN uv export --no-dev --format requirements.txt >> requirements.txt


FROM python:3.13-slim-bullseye

WORKDIR /app

RUN mkdir -p /app/data

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --index-url https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r /app/requirements.txt

COPY ./beetle /app/beetle
COPY ./migrations /app/migrations

CMD ["granian", "--access-log", "--host", "0.0.0.0", "--interface", "asgi", "beetle.main:app"]