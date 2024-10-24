#!/bin/bash

# Exit script if you try to use an uninitialized variable.
set -o nounset

# Exit script if a statement returns a non-true return value.
set -o errexit

# Use the error status of the first failure, rather than that of the last item in a pipeline.
set -o pipefail

# Ensure all required arguments are provided
if [ "$#" -ne 6 ]; then
    echo "Usage: $0 ACCESS_KEY SECRET_KEY AWS_DEFAULT_REGION AWS_ECR_ACCOUNT_URL KUBECONFIG CLUSTER"
    exit 1
fi

# Assign arguments to variables
ACCESS_KEY=$1
SECRET_KEY=$2
AWS_DEFAULT_REGION=$3
AWS_ECR_ACCOUNT_URL=$4
KUBECONFIG=$5
CLUSTER=$6

aws configure set aws_access_key_id $ACCESS_KEY
aws configure set aws_secret_access_key $SECRET_KEY
aws configure set output "json"
PASS=$(aws ecr get-login-password --region $AWS_DEFAULT_REGION)
echo ${AWS_ECR_ACCOUNT_URL}
docker login -u AWS -p ${PASS} ${AWS_ECR_ACCOUNT_URL}

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp && sudo mv /tmp/eksctl /usr/local/bin

# Install and configure kubectl aws-iam-authenticator
curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.5.9/aws-iam-authenticator_0.5.9_linux_amd64 && chmod +x ./aws-iam-authenticator && mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$PATH:$HOME/bin

#configure kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Decode Kubeconfig
echo $KUBECONFIG | base64 -d > kubeconfig

export KUBECONFIG=./kubeconfig

#configure helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod +x get_helm.sh
./get_helm.sh

#Configure kubectl
aws eks --region $AWS_DEFAULT_REGION update-kubeconfig --name $CLUSTER

# login to ECR, build image and push to registry
make push

kubectl get svc

# Deploy app to K8s cluster with helm
make deploy

# Clean up resources
make clean
