# LLM Benchmarking Simulation
This tool benchmarks the performance of various Language Learning Models (LLMs) against several quality metrics such as Time to First Token (TTFT), Tokens Per Second (TPS), End-to-End Latency (e2e_latency), and Requests Per Second (RPS). It consists of two services; a randomiser which simulates and stores 1000 values for each llm based on the specified metrics. Deployment is handled using helm to a kubernetes cluster. The pipeline created natively supports deployment to an EKS cluster, using ECR as a container registry.

## Features
- Simulates and benchmarks LLMs.
- Exposes API endpoints to fetch benchmark results and LLM rankings.
- Robust and scalable deployment with Kubernetes using Helm charts.
- Seeds model records on startup
- Retries failed operations
- Create additional LLMs and metrics

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

3. Set up your `.env` file with the necessary environment variables

4. Run database migrations:
   `make migrate`
<br>
5. Start the services:
    Randomiser: 

   `make start-randomiser`

   Benchmark API (In a separate terminal):

   `make start-api`


### Using Docker Compose
1. Set up your `.env` file with the necessary environment variables
```
cp .env.example .env
```

2. In the root of the project directory, run:
```bash
docker-compose up --build -d
```

To run in one command (if .env doesn't exist):
```
cp .env.example .env && docker-compose up --build -d
```

3. Migrations should run automatically. In case you need to run commands once inside the container, you can run migrations (for example) using:
```bash
alembic upgrade head
```

or outside the container using:
```bash
docker-compose exec randomiser_service alembic upgrade head
```

## Kubernetes Deployment

1. Set up a Kubernetes cluster and store the configured kubecofng in your kube root.

2. Install Helm v3:
   ```
   curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
   ```

## API 

To View the Swagger UI API documentation, visit `http://localhost:8001/docs`.

The Benchmark API application exposes the following endpoints:

### Get LLMs
- GET /api/v1/llms -  Returns the list of LLMs.

#### Example:
```bash
curl -X 'GET' \
  'http://localhost:8001/api/v1/llms' \
  -H 'accept: application/json' \
  -H 'api-key: 1'
```

### Response:
```json
{
    "status": "success",
    "data": [
        {
            "id": "50fc245a-0f2b-4086-8c61-672f125f48e4",
            "created_at": "2024-10-24T10:53:28.282048Z",
            "name": "GPT-4o",
            "creator": "OpenAI",
            "updated_at": null
        },
        {
            "id": "7d8788fb-c91e-450d-ad08-dd291de9918d",
            "created_at": "2024-10-24T10:53:28.282048Z",
            "name": "Llama 3.1 405",
            "creator": "Meta",
            "updated_at": null
        },
        {
            "id": "bdb8a134-16cf-4054-bc44-32ad304d98db",
            "created_at": "2024-10-24T10:53:28.282048Z",
            "name": "Claude 3.5 Sonnet",
            "creator": "Anthropic",
            "updated_at": null
        },
        {
            "id": "e7a8a618-8bb5-4e2c-b7c7-20448e8e3e85",
            "created_at": "2024-10-24T10:53:28.282048Z",
            "name": "Gemini 1.5Flash",
            "creator": "Google",
            "updated_at": null
        }
    ]
}
```

### Create LLM
- POST /api/v1/llms - Adds a new LLM.

#### Example:
```bash
curl -X POST \
  'http://localhost:8001/api/v1/llms' \
  -H 'accept: application/json' \
  -H 'api-key: 1' \
  -d '{
    "name": "Mixtral 8x22B",
    "creator": "Mistral AI"
    }'
```

### Response:
```json
{
    "status": "success",
    "data": {
        "id": "1936720d-6153-4e37-8df2-ae28008ed06f",
        "created_at": "2024-10-24T22:06:00.526653Z",
        "name": "Mixtral 8x22B",
        "creator": "Mistral AI",
        "updated_at": null
    }
}
```

### Get Metrics
- GET /api/v1/metrics -  Returns the list of metrics.

#### Example:
```bash
curl -X 'GET' \
  'http://localhost:8001/api/v1/metrics' \
  -H 'accept: application/json' \
  -H 'api-key: 1'
```

### Response:
```json
{
    "status": "success",
    "data": [
        {
            "id": "b60262b8-3983-46ef-b282-adbe1aa88c6d",
            "created_at": "2024-10-24T11:01:57.624538+00:00",
            "title": "ttft",
            "upper_bound": 2,
            "lower_bound": 0.05,
            "updated_at": null
        },
        {
            "id": "642f0b9f-b76f-4d09-9e4d-3c25bb874a30",
            "created_at": "2024-10-24T11:01:57.624538+00:00",
            "title": "tps",
            "upper_bound": 150,
            "lower_bound": 10,
            "updated_at": null
        },
        {
            "id": "7e258821-00bb-4d27-9756-a9ee62027044",
            "created_at": "2024-10-24T11:01:57.624538+00:00",
            "title": "e2e_latency",
            "upper_bound": 10,
            "lower_bound": 0.2,
            "updated_at": null
        },
        {
            "id": "f205e206-8b4e-4d68-a113-e5288d11647a",
            "created_at": "2024-10-24T11:01:57.624538+00:00",
            "title": "rps",
            "upper_bound": 100,
            "lower_bound": 1,
            "updated_at": null
        }
    ]
}
```

### Create Metric
- POST /api/v1/metrics - Adds a new Metric.

#### Example:
```bash
curl -X POST \
  'http://localhost:8001/api/v1/metrics' \
  -H 'accept: application/json' \
  -H 'api-key: 1' \
  -d '{
    "title": "gpqa",
    "upper_bound": 100.0,
    "lower_bound": 0.0
    }'
```

### Response:
```json
{
    "status": "success",
    "data": {
        "id": "c3400ef8-3146-4b88-b6ac-21797591cde1",
        "created_at": "2024-10-24T22:18:38.999586Z",
        "title": "gpqa",
        "upper_bound": 100.0,
        "lower_bound": 0.0,
        "updated_at": null
    }
}
```

### Get All LLM Rankings
- GET /api/v1/rankings/{metric} -  Returns all LLM rankings.

#### Example:
```bash
curl -X 'GET' \
  'http://localhost:8001/api/v1/benchmarks/rankings' \
  -H 'accept: application/json' \
  -H 'api-key: 1'
```

### Response:
```json
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
```json
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

