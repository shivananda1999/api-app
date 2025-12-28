#!/bin/bash

# AWS Deployment Script for FastAPI Streaming Application
# This script automates the deployment process to AWS EKS

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-""}
ECR_REPOSITORY=${ECR_REPOSITORY:-fastapi-streaming}
EKS_CLUSTER_NAME=${EKS_CLUSTER_NAME:-streaming-cluster}
IMAGE_TAG=${IMAGE_TAG:-v1}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AWS Deployment...${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if eksctl is installed
if ! command -v eksctl &> /dev/null; then
    echo -e "${YELLOW}eksctl is not installed. Installing...${NC}"
    # Install eksctl (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap weaveworks/tap
        brew install weaveworks/tap/eksctl
    else
        echo -e "${RED}Please install eksctl manually.${NC}"
        exit 1
    fi
fi

# Get AWS Account ID if not set
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo -e "${YELLOW}Getting AWS Account ID...${NC}"
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo -e "${GREEN}AWS Account ID: $AWS_ACCOUNT_ID${NC}"
fi

# Step 1: Create ECR Repository
echo -e "${GREEN}Step 1: Creating ECR Repository...${NC}"
aws ecr create-repository \
    --repository-name $ECR_REPOSITORY \
    --region $AWS_REGION \
    --image-scanning-configuration scanOnPush=true \
    || echo -e "${YELLOW}Repository already exists${NC}"

# Step 2: Authenticate Docker to ECR
echo -e "${GREEN}Step 2: Authenticating Docker to ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 3: Build and Push Docker Image
echo -e "${GREEN}Step 3: Building Docker Image...${NC}"
docker build -t $ECR_REPOSITORY:$IMAGE_TAG .

echo -e "${GREEN}Tagging Image...${NC}"
docker tag $ECR_REPOSITORY:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

echo -e "${GREEN}Pushing Image to ECR...${NC}"
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

# Step 4: Update Kubernetes deployment with image
echo -e "${GREEN}Step 4: Updating Kubernetes manifests...${NC}"
sed -i.bak "s|YOUR_ACCOUNT_ID|$AWS_ACCOUNT_ID|g" kubernetes/aws-deployment.yaml
rm kubernetes/aws-deployment.yaml.bak

# Step 5: Check if EKS cluster exists
echo -e "${GREEN}Step 5: Checking EKS Cluster...${NC}"
if ! eksctl get cluster --name $EKS_CLUSTER_NAME --region $AWS_REGION &> /dev/null; then
    echo -e "${YELLOW}EKS Cluster not found. Creating cluster...${NC}"
    echo -e "${YELLOW}Note: This will create a t3.micro cluster (Free Tier compatible)${NC}"
    echo -e "${YELLOW}For GPU support, you'll need to add a GPU node group separately${NC}"
    
    eksctl create cluster \
        --name $EKS_CLUSTER_NAME \
        --region $AWS_REGION \
        --nodegroup-name standard-nodes \
        --node-type t3.micro \
        --nodes 2 \
        --nodes-min 1 \
        --nodes-max 3 \
        --managed
else
    echo -e "${GREEN}EKS Cluster exists. Updating kubeconfig...${NC}"
    aws eks update-kubeconfig --name $EKS_CLUSTER_NAME --region $AWS_REGION
fi

# Step 6: Install NVIDIA Device Plugin (if GPU nodes exist)
echo -e "${GREEN}Step 6: Installing NVIDIA Device Plugin (if needed)...${NC}"
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml || \
    echo -e "${YELLOW}NVIDIA Device Plugin installation skipped (no GPU nodes)${NC}"

# Step 7: Deploy Application
echo -e "${GREEN}Step 7: Deploying Application...${NC}"
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/aws-deployment.yaml
kubectl apply -f kubernetes/aws-service.yaml
kubectl apply -f kubernetes/aws-hpa.yaml

# Step 8: Wait for deployment
echo -e "${GREEN}Step 8: Waiting for deployment to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/fastapi-streaming -n fastapi-streaming

# Step 9: Get service endpoint
echo -e "${GREEN}Step 9: Getting service endpoint...${NC}"
kubectl get svc fastapi-streaming-service -n fastapi-streaming

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${YELLOW}Note: It may take a few minutes for the LoadBalancer to get an external IP${NC}"
echo -e "${YELLOW}Use 'kubectl get svc -n fastapi-streaming' to check the status${NC}"

