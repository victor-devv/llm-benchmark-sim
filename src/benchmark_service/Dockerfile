FROM python:3.12-slim

ENV POETRY_VERSION=1.8.4
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

COPY ../ /app

RUN poetry install --no-root --no-dev --no-update

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.benchmark_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
