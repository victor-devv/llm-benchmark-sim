# LLM Benchmarking Simulation
This tool benchmarks the performance of various Language Learning Models (LLMs) against several quality metrics such as Time to First Token (TTFT), Tokens Per Second (TPS), End-to-End Latency (e2e_latency), and Requests Per Second (RPS). It consists of two services; a randomiser which simulates and stores 1000 values for each llm based on the specified metrics. Deployment is handled using helm to a kubernetes cluster. The pipeline created natively supports deployment to an EKS cluster, using ECR as a container registry

## Features
- Simulates and benchmarks LLMs.
- Exposes API endpoints to fetch benchmark results and LLM rankings.
- Robust and scalable deployment with Kubernetes using Helm charts.
- Seeds model records on startup
- Retries failed operations

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
- AWS EKS
- AWS ECR

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


## API 

To View the Swagger UI API documentation, visit `http://localhost:8001/docs`.

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

### Response:
```
{
    "status": "success",
    "data": [
        {
            "ttft": [
                {
                    "llm": "Gemini 1.5Flash",
                    "mean": 1.05
                },
                {
                    "llm": "GPT-4o",
                    "mean": 1.03
                },
                {
                    "llm": "Llama 3.1 405",
                    "mean": 1.03
                },
                {
                    "llm": "Claude 3.5 Sonnet",
                    "mean": 1.02
                }
            ]
        },
        {
            "tps": [
                {
                    "llm": "GPT-4o",
                    "mean": 82.91
                },
                {
                    "llm": "Gemini 1.5Flash",
                    "mean": 80.32
                },
                {
                    "llm": "Claude 3.5 Sonnet",
                    "mean": 78.69
                },
                {
                    "llm": "Llama 3.1 405",
                    "mean": 78.3
                }
            ]
        },
        {
            "e2e_latency": [
                {
                    "llm": "Claude 3.5 Sonnet",
                    "mean": 5.16
                },
                {
                    "llm": "Llama 3.1 405",
                    "mean": 5.16
                },
                {
                    "llm": "GPT-4o",
                    "mean": 5.05
                },
                {
                    "llm": "Gemini 1.5Flash",
                    "mean": 5.04
                }
            ]
        },
        {
            "rps": [
                {
                    "llm": "GPT-4o",
                    "mean": 50.77
                },
                {
                    "llm": "Llama 3.1 405",
                    "mean": 50.35
                },
                {
                    "llm": "Claude 3.5 Sonnet",
                    "mean": 50.12
                },
                {
                    "llm": "Gemini 1.5Flash",
                    "mean": 48.32
                }
            ]
        }
    ]
}
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

### Response:
```
{
    "status": "success",
    "data": [
        {
            "llm": "Gemini 1.5Flash",
            "mean": 1.05
        },
        {
            "llm": "GPT-4o",
            "mean": 1.03
        },
        {
            "llm": "Llama 3.1 405",
            "mean": 1.03
        },
        {
            "llm": "Claude 3.5 Sonnet",
            "mean": 1.02
        }
    ]
}
```
### Kubernetes Deployment

- Step 1: Install Helm
Make sure Helm is installed. You can install it by running:
```bash 
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

- Step 2: Deploy the Application
Initialize a Kubernetes cluster if not already running (use minikube, Docker Desktop, or any cloud Kubernetes provider).

##### Local Deployment:
```bash
make deploy-local
```

## Remote Deployment
Whenever changes are pushed or merged to the main branch of this repository, the GitHub Actions workflow will automatically trigger build and deployment.
Ensure all required workflow secrets are properly set up as well as the EKS cluster and ECR repository.
The deployment will be exposed through an ingress as the service type is a ClusterIP.

