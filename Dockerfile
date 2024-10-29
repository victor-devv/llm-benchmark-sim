FROM python:3.12-slim

ENV POETRY_VERSION=1.8.4
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.benchmark_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
