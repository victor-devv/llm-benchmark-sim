FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV POETRY_VERSION=1.8.4
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

RUN poetry lock --no-update
RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.benchmark_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
