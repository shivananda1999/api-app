# FastAPI Streaming Application

A production-ready FastAPI-based streaming application with 10 endpoints, designed for GPU-accelerated inference and deployment on AWS EKS, GCP GKE, and local Docker environments.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Local Docker Deployment](#local-docker-deployment)
- [AWS EKS Deployment](#aws-eks-deployment)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Testing](#testing)
- [Cost Optimization](#cost-optimization)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **10 Streaming Endpoints**: Text, Audio, Video, Data, Logs, Metrics, Chat, Transcription, Translation, and Analysis
- **Rate Limiting**: 100 requests/minute per IP address
- **Authentication**: API Key-based authentication
- **CORS Support**: Cross-origin resource sharing enabled
- **Request Validation**: Pydantic models for all endpoints
- **OpenAPI Documentation**: Auto-generated Swagger/ReDoc docs
- **GPU Support**: Optional GPU acceleration for model inference
- **High Availability**: Kubernetes deployment with auto-scaling
- **Load Balancing**: Nginx reverse proxy configuration

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│   Nginx     │ (Load Balancer)
└──────┬──────┘
       │
┌──────▼──────┐
│   FastAPI   │ (Application)
└──────┬──────┘
       │
┌──────▼──────┐
│   GPU/CPU   │ (Inference)
└─────────────┘
```

## 📦 Prerequisites

### For Local Development
- Python 3.11+
- Docker Desktop / Docker Engine
- Docker Compose v2.0+
- (Optional) NVIDIA GPU with drivers and NVIDIA Container Toolkit

### For AWS Deployment
- AWS Account (Free Tier eligible)
- AWS CLI v2 installed and configured
- `eksctl` CLI installed
- `kubectl` CLI installed
- Docker installed locally

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd api-app
```

### 2. Create Environment File

```bash
cp .env.example .env
# Edit .env and set your API_KEY
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐳 Local Docker Deployment

### CPU-Only Mode

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### GPU-Enabled Mode

**Prerequisites:**
- NVIDIA GPU with drivers installed
- NVIDIA Container Toolkit installed

```bash
# Install NVIDIA Container Toolkit (Linux)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Run with GPU support
docker-compose -f docker-compose.gpu.yml up -d --build

# Verify GPU access
docker exec fastapi-streaming-gpu nvidia-smi
```

### Scale Replicas

```bash
docker-compose up -d --scale fastapi=3
```

## ☁️ AWS EKS Deployment

### Free Tier Considerations

**Important Notes:**
- GPU instances (g4dn, p3) are **NOT** included in AWS Free Tier
- Use `t3.micro` instances for initial testing (Free Tier eligible)
- EKS cluster itself has costs (~$0.10/hour for control plane)
- Set up billing alerts before deployment
- Delete resources immediately after testing

### Step-by-Step Deployment

#### Option 1: Automated Script (Recommended)

```bash
# Set environment variables
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export ECR_REPOSITORY=fastapi-streaming
export EKS_CLUSTER_NAME=streaming-cluster

# Run deployment script
./scripts/deploy-aws.sh
```

#### Option 2: Manual Deployment

**Step 1: Create ECR Repository**

```bash
aws ecr create-repository \
    --repository-name fastapi-streaming \
    --region us-east-1 \
    --image-scanning-configuration scanOnPush=true
```

**Step 2: Authenticate Docker to ECR**

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

**Step 3: Build and Push Image**

```bash
# Build
docker build -t fastapi-streaming:v1 .

# Tag
docker tag fastapi-streaming:v1 $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fastapi-streaming:v1

# Push
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fastapi-streaming:v1
```

**Step 4: Create EKS Cluster (Free Tier Compatible)**

```bash
# Create cluster with t3.micro nodes (Free Tier)
eksctl create cluster \
    --name streaming-cluster \
    --region us-east-1 \
    --nodegroup-name standard-nodes \
    --node-type t3.micro \
    --nodes 2 \
    --nodes-min 1 \
    --nodes-max 3 \
    --managed

# Update kubeconfig
aws eks update-kubeconfig --name streaming-cluster --region us-east-1
```

**Step 5: Update Kubernetes Manifests**

Edit `kubernetes/aws-deployment.yaml` and replace `YOUR_ACCOUNT_ID` with your AWS Account ID:

```bash
sed -i.bak "s|YOUR_ACCOUNT_ID|$AWS_ACCOUNT_ID|g" kubernetes/aws-deployment.yaml
```

**Step 6: Deploy Application**

```bash
# Apply all manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/aws-deployment.yaml
kubectl apply -f kubernetes/aws-service.yaml
kubectl apply -f kubernetes/aws-hpa.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=300s \
    deployment/fastapi-streaming -n fastapi-streaming

# Check status
kubectl get pods -n fastapi-streaming
kubectl get svc -n fastapi-streaming
```

**Step 7: Get Service Endpoint**

```bash
# Get LoadBalancer external IP
kubectl get svc fastapi-streaming-service -n fastapi-streaming

# It may take 2-5 minutes for the LoadBalancer to get an external IP
```

### Adding GPU Support (Optional - Not Free Tier)

If you need GPU support and have budget:

```bash
# Add GPU node group
eksctl create nodegroup \
    --cluster streaming-cluster \
    --region us-east-1 \
    --name gpu-nodes \
    --node-type g4dn.xlarge \
    --nodes 1 \
    --nodes-min 1 \
    --nodes-max 2 \
    --managed

# Install NVIDIA Device Plugin
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml

# Update deployment to use GPU (uncomment GPU resources in aws-deployment.yaml)
kubectl apply -f kubernetes/aws-deployment.yaml
```

### Cost Optimization Tips

1. **Use Spot Instances**: 60-90% cost savings
   ```bash
   eksctl create nodegroup --spot --instance-types=t3.micro
   ```

2. **Set Up Billing Alerts**
   ```bash
   aws budgets create-budget \
       --account-id $AWS_ACCOUNT_ID \
       --budget file://budget.json \
       --notifications-with-subscribers file://notifications.json
   ```

3. **Use Smaller Instance Types**: t3.micro for testing
4. **Delete Unused Resources**: Always clean up after testing
5. **Use Reserved Instances**: For long-term deployments

### Cleanup

```bash
# Delete EKS cluster
eksctl delete cluster --name streaming-cluster --region us-east-1

# Delete ECR repository
aws ecr delete-repository \
    --repository-name fastapi-streaming \
    --region us-east-1 \
    --force
```

## 📡 API Endpoints

All endpoints require authentication via `X-API-Key` header.

Base URL: `http://localhost:8000` (local) or your LoadBalancer URL (AWS)

### 1. Stream Text
```bash
POST /api/v1/stream/text
Content-Type: application/json
X-API-Key: your-api-key

{
  "text": "This is a sample text to stream",
  "chunk_size": 10
}
```

### 2. Stream Audio
```bash
POST /api/v1/stream/audio
Content-Type: application/json
X-API-Key: your-api-key

{
  "audio_url": "https://example.com/audio.wav",
  "sample_rate": 44100
}
```

### 3. Stream Video
```bash
POST /api/v1/stream/video
Content-Type: application/json
X-API-Key: your-api-key

{
  "video_url": "https://example.com/video.mp4",
  "fps": 30
}
```

### 4. Stream Data
```bash
POST /api/v1/stream/data
Content-Type: application/json
X-API-Key: your-api-key

{
  "data": {"key1": "value1", "key2": "value2"},
  "format": "json"
}
```

### 5. Stream Logs
```bash
POST /api/v1/stream/logs
Content-Type: application/json
X-API-Key: your-api-key

{
  "log_level": "INFO",
  "lines": 100
}
```

### 6. Stream Metrics
```bash
GET /api/v1/stream/metrics
X-API-Key: your-api-key
```

### 7. Stream Chat
```bash
POST /api/v1/stream/chat
Content-Type: application/json
X-API-Key: your-api-key

{
  "message": "Hello, how are you?",
  "model": "gpt-3.5-turbo"
}
```

### 8. Stream Transcription
```bash
POST /api/v1/stream/transcription
Content-Type: application/json
X-API-Key: your-api-key

{
  "audio_url": "https://example.com/audio.wav",
  "language": "en"
}
```

### 9. Stream Translation
```bash
POST /api/v1/stream/translation
Content-Type: application/json
X-API-Key: your-api-key

{
  "text": "Hello, world!",
  "source_lang": "en",
  "target_lang": "es"
}
```

### 10. Stream Analysis
```bash
POST /api/v1/stream/analysis
Content-Type: application/json
X-API-Key: your-api-key

{
  "content": "This is a sample text for analysis",
  "analysis_type": "sentiment"
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
API_KEY=your-secure-api-key-here
ENVIRONMENT=production
LOG_LEVEL=INFO
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your-account-id
ECR_REPOSITORY=fastapi-streaming
EKS_CLUSTER_NAME=streaming-cluster
```

### Kubernetes ConfigMap

Edit `kubernetes/configmap.yaml` to update configuration:

```yaml
data:
  API_KEY: "your-api-key"
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
```

## 🧪 Testing

### Using curl

```bash
# Health check (no auth required)
curl http://localhost:8000/health

# Test endpoint with API key
curl -X POST http://localhost:8000/api/v1/stream/text \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-12345-change-in-production" \
  -d '{"text": "Hello World", "chunk_size": 5}'
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/v1/stream/text"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "dev-api-key-12345-change-in-production"
}
data = {
    "text": "This is a test",
    "chunk_size": 10
}

response = requests.post(url, json=data, headers=headers, stream=True)
for chunk in response.iter_content(chunk_size=128):
    print(chunk.decode('utf-8'))
```

### Load Testing

```bash
# Install Apache Bench
# macOS: brew install httpd
# Linux: apt-get install apache2-utils

# Test rate limiting
ab -n 200 -c 10 -H "X-API-Key: dev-api-key-12345-change-in-production" \
   http://localhost:8000/api/v1/stream/metrics
```

## 💰 Cost Optimization

### AWS Free Tier Limits

- **EC2**: 750 hours/month of t2.micro or t3.micro
- **EBS**: 30 GB storage
- **Data Transfer**: 15 GB outbound
- **EKS**: Control plane costs ~$0.10/hour (not free)

### Cost-Saving Strategies

1. **Use Spot Instances**: 60-90% savings
2. **Right-size Instances**: Use t3.micro for testing
3. **Set Auto-scaling**: Scale down during low usage
4. **Delete Unused Resources**: Clean up after testing
5. **Use Reserved Instances**: For production (1-3 year terms)

### Estimated Monthly Costs (Free Tier)

- **EKS Control Plane**: ~$72/month (always running)
- **t3.micro Nodes (2)**: Free (750 hours/month)
- **LoadBalancer**: ~$16/month
- **ECR Storage**: ~$0.10/month (minimal)
- **Total**: ~$88/month (with Free Tier EC2)

**Note**: Delete the cluster when not in use to save costs!

## 🔧 Troubleshooting

### Common Issues

#### 1. Rate Limit Exceeded
```
HTTP 429: Rate limit exceeded
```
**Solution**: Wait 1 minute or increase rate limit in code

#### 2. Invalid API Key
```
HTTP 403: Invalid API key
```
**Solution**: Check `X-API-Key` header matches `.env` file

#### 3. Docker Build Fails
```
Error: failed to solve
```
**Solution**: Check Docker is running and has enough resources

#### 4. EKS Cluster Creation Fails
```
Error: insufficient capacity
```
**Solution**: Try different region or instance type

#### 5. Pods Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name> -n fastapi-streaming

# Check logs
kubectl logs <pod-name> -n fastapi-streaming
```

#### 6. LoadBalancer Pending
```bash
# Check service
kubectl describe svc fastapi-streaming-service -n fastapi-streaming

# May take 2-5 minutes for AWS to provision
```

## 📝 Work Summary Template

Use this template to document your deployment:

```
CANDIDATE WORK SUMMARY
────────────────────────────────────────────
Candidate Name: _______________________
Date Submitted: _______________________
Total Time Spent: _______ hours
Repository URL: _______________________

1. DEPLOYMENT STATUS
   [ ] Local Docker (CPU)
   [ ] Local Docker (GPU)
   [ ] AWS EKS (Free Tier)
   [ ] AWS EKS (GPU)

2. CHALLENGES FACED
   Describe any significant challenges and how you resolved them:
   _____________________________________________________________

3. ARCHITECTURE DECISIONS
   Explain key architecture/design decisions made:
   _____________________________________________________________

4. COST BREAKDOWN
   AWS Credits Used: $_______
   Cost optimization strategies implemented: _________________________

5. IMPROVEMENTS FOR PRODUCTION
   List improvements you would make for a production deployment:
   _____________________________________________________________
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks)
- [Docker Documentation](https://docs.docker.com)
- [Kubernetes Documentation](https://kubernetes.io/docs)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native)

## 📄 License

This project is for assessment purposes.

## 🤝 Contributing

This is an assessment project. For questions or issues, please refer to the assessment guidelines.

---

**Important**: Always set up billing alerts and delete resources after testing to avoid unexpected charges!

