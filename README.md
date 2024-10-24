# LLM Benchmarking Simulation
This tool benchmarks the performance of various Language Learning Models (LLMs) against several quality metrics such as Time to First Token (TTFT), Tokens Per Second (TPS), End-to-End Latency (e2e_latency), and Requests Per Second (RPS). It consists of two services; a randomiser which simulates and stores 1000 values for each llm based on the specified metrics. Deployment is handled using helm to a kubernetes cluster.

## Features
- Simulates and benchmarks LLMs.
- Exposes API endpoints to fetch benchmark results and LLM rankings.
- Robust and scalable deployment with Kubernetes using Helm charts.
- Integrated monitoring with Prometheus and Grafana for metrics tracking and alerts.


# Installation
## Prerequisites
- Docker
- Docker Compose
- Kubernetes
- Helm 3+
- Python 3.12+
- Poetry 1.8.4
- PostgreSQL 17
- Prometheus 
- Grafana

## Clone the repository
  ```bash
    git clone https://github.com/victor-devv/llm-benchmark-sim.git
    cd llm-benchmark-sim
    cp .env.example .env
  ```

## Running the Application

### Local Development


1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies: (Ensure Poetry is installed)
   `make install`
<br>

3. Set up your `.env` file with the necessary environment variables:

4. Run database migrations:
   `make migrate`
<br>
5. Start the services:
    Randomiser: 

   `make start-randomiser`

   Benchmark API (In a separate terminal):

   `make start-api`


### Using Docker Compose
In the root of the project directory, run:
```bash
docker-compose up --build -d
```
- Once inside the container, you can run Alembic migrations 
```bash
  alembic upgrade head
```
- or run this command:
```bash
docker-compose exec api alembic upgrade head
```

## Kubernetes Deployment

1. Set up a Kubernetes cluster and store the configured kubecofng in your kube root.

2. Install Helm v3:
   ```
   curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
   ```
  or `brew install helm`


## API Endpoints
The Benchmark API application exposes the following endpoints:

### Get Metrics
- GET /api/v1/metrics -  Returns the list of metrics.

#### Example:
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/metrics' \
  -H 'accept: application/json' \
  -H 'api-key: 1'
```

### Get All LLM Rankings
- GET /api/v1/rankings/{metric} -  Returns all LLM rankings.

#### Example:
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/benchmarks/rankings' \
  -H 'accept: application/json' \
  -H 'api-key: 1'
```

### Get LLM Rankings by Metric
- GET /api/v1/benchmarks/rankings/{metric} -  Returns all LLM ranking of LLMs for a specified metric.

#### Example:
```bash
curl -X 'GET' \
  'http://localhost:8001/api/v1/benchmarks/rankings/ttft' \
  -H 'accept: application/json' \
  -H 'api-key: 1'
```
