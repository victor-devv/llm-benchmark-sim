#!/bin/bash

set -a
source .env
set +a

cd ./charts

helm dependency update

cd ..

# Generate a values file from .env
cat <<EOF > charts/values_overrides.yaml
secrets:
  POSTGRES_PASSWORD: "$POSTGRES_PASSWORD"
  API_KEY: "$API_KEY"
EOF

helm upgrade --install chart ./llm_benchmark_chart \
  --values charts/values_overrides.yaml
