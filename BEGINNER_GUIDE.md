# 🎓 Complete Beginner's Guide - Step by Step

This guide will walk you through the entire project from scratch. Follow each step in order, and you'll have a fully deployed FastAPI streaming application!

## 📋 Table of Contents

1. [Prerequisites Check](#step-1-prerequisites-check)
2. [Project Setup](#step-2-project-setup)
3. [Understanding the Project](#step-3-understanding-the-project)
4. [Local Development](#step-4-local-development)
5. [Testing Locally](#step-5-testing-locally)
6. [Docker Deployment](#step-6-docker-deployment)
7. [AWS Account Setup](#step-7-aws-account-setup)
8. [AWS Deployment](#step-8-aws-deployment)
9. [Verification & Testing](#step-9-verification--testing)
10. [Cleanup](#step-10-cleanup)
11. [Troubleshooting](#troubleshooting)

---

## Step 1: Prerequisites Check

Before starting, make sure you have these installed on your computer.

### 1.1 Check Python Installation

Open your terminal (Mac: Terminal, Windows: Command Prompt or PowerShell) and run:

```bash
python3 --version
```

**Expected output:** Python 3.11 or higher

**If not installed:**
- Mac: `brew install python3`
- Windows: Download from https://www.python.org/downloads/
- Linux: `sudo apt-get install python3`

### 1.2 Check pip Installation

```bash
pip3 --version
```

**If not installed:** Usually comes with Python. If missing, install pip.

### 1.3 Check Docker Installation

```bash
docker --version
```

**Expected output:** Docker version 20.x or higher

**If not installed:**
- Mac: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Windows: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Linux: `sudo apt-get install docker.io`

**Start Docker Desktop** (if using Mac/Windows) - make sure it's running!

### 1.4 Check Git Installation

```bash
git --version
```

**If not installed:**
- Mac: `brew install git`
- Windows: Download from https://git-scm.com/download/win
- Linux: `sudo apt-get install git`

### 1.5 Check AWS CLI (for AWS deployment)

```bash
aws --version
```

**If not installed:**
- Mac: `brew install awscli`
- Windows: Download from https://aws.amazon.com/cli/
- Linux: `sudo apt-get install awscli`

**Configure AWS CLI:**
```bash
aws configure
```

You'll need:
- AWS Access Key ID (from AWS Console → IAM → Users → Security Credentials)
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

### 1.6 Install eksctl (for AWS EKS)

```bash
eksctl version
```

**If not installed:**
- Mac: `brew tap weaveworks/tap && brew install weaveworks/tap/eksctl`
- Windows: Download from https://github.com/weaveworks/eksctl/releases
- Linux: Follow instructions at https://eksctl.io/introduction/#installation

### 1.7 Install kubectl (for Kubernetes)

```bash
kubectl version --client
```

**If not installed:**
- Mac: `brew install kubectl`
- Windows: Download from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
- Linux: `sudo apt-get install kubectl`

---

## Step 2: Project Setup

### 2.1 Navigate to Project Directory

Open terminal and go to your project folder:

```bash
cd /Users/macbook/Documents/poc/api-app
```

**Verify you're in the right place:**
```bash
ls
```

You should see files like `README.md`, `requirements.txt`, `Dockerfile`, etc.

### 2.2 Create Python Virtual Environment

A virtual environment keeps your project dependencies separate from other projects.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

**You'll see `(venv)` in your terminal prompt** - this means it's active!

### 2.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

**This will take 2-5 minutes.** It's installing all the Python packages needed for the project.

**Expected output:** "Successfully installed..." messages

### 2.4 Create Environment File

```bash
# Copy the example file
cp env.example .env

# Edit the .env file (use any text editor)
# On Mac/Linux:
nano .env

# On Windows:
notepad .env
```

**Set your API key** (you can use the default for testing):
```
API_KEY=dev-api-key-12345-change-in-production
```

**Save and close** the file (Ctrl+X, then Y, then Enter for nano).

---

## Step 3: Understanding the Project

### 3.1 What This Project Does

This is a **FastAPI streaming application** with 10 endpoints that can:
- Stream text, audio, video, data
- Stream logs and metrics
- Stream chat responses
- Stream transcriptions and translations
- Stream analysis results

### 3.2 Project Structure

```
api-app/
├── app/                    # Main application code
│   ├── main.py            # Entry point with 10 endpoints
│   ├── middleware/        # Authentication code
│   ├── models/           # Data validation models
│   └── routers/          # Individual endpoint logic
├── kubernetes/           # Kubernetes deployment files
├── scripts/             # Helper scripts
├── Dockerfile           # Docker image for CPU
├── Dockerfile.gpu       # Docker image for GPU
├── docker-compose.yml   # Local Docker setup
└── requirements.txt     # Python dependencies
```

### 3.3 Key Files Explained

- **app/main.py**: The main FastAPI application with all 10 endpoints
- **requirements.txt**: List of Python packages needed
- **Dockerfile**: Instructions to build a Docker container
- **docker-compose.yml**: Configuration to run multiple containers together
- **kubernetes/**: Files to deploy on AWS EKS (Kubernetes)

---

## Step 4: Local Development

### 4.1 Start the Application

Make sure your virtual environment is activated (you see `(venv)` in terminal):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**What this does:**
- `uvicorn`: The web server that runs FastAPI
- `app.main:app`: Tells it to run the `app` from `app/main.py`
- `--reload`: Automatically restarts when you change code (for development)
- `--host 0.0.0.0`: Makes it accessible from any network interface
- `--port 8000`: Runs on port 8000

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal window open!** The server is running.

### 4.2 Test the Application

Open a **new terminal window** (keep the server running in the first one) and test:

```bash
# Health check (no authentication needed)
curl http://localhost:8000/health
```

**Expected output:**
```json
{"status":"healthy","service":"fastapi-streaming"}
```

### 4.3 View API Documentation

Open your web browser and go to:

**Swagger UI (Interactive):**
```
http://localhost:8000/docs
```

**ReDoc (Alternative):**
```
http://localhost:8000/redoc
```

**You can test all endpoints directly in the browser!**

### 4.4 Test an Endpoint

In the browser at `http://localhost:8000/docs`:

1. Click on **POST /api/v1/stream/text**
2. Click **"Try it out"**
3. Enter this in the request body:
```json
{
  "text": "Hello World, this is a test",
  "chunk_size": 5
}
```
4. Click **"Execute"**
5. You should see streaming text output!

**Or use curl in terminal:**
```bash
curl -X POST http://localhost:8000/api/v1/stream/text \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-12345-change-in-production" \
  -d '{"text": "Hello World", "chunk_size": 5}'
```

### 4.5 Stop the Server

When you're done testing, go back to the terminal where the server is running and press:
```
Ctrl + C
```

This stops the server.

---

## Step 5: Testing Locally

### 5.1 Run the Test Script

We have a script that tests all 10 endpoints automatically:

```bash
# Make sure the server is running first (Step 4.1)
# Then in a new terminal:
./scripts/test-api.sh
```

**If you get "Permission denied":**
```bash
chmod +x scripts/test-api.sh
./scripts/test-api.sh
```

**Expected output:** Tests for all 10 endpoints with status messages.

### 5.2 Manual Testing

You can test each endpoint manually. Here are examples:

**1. Stream Text:**
```bash
curl -X POST http://localhost:8000/api/v1/stream/text \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-12345-change-in-production" \
  -d '{"text": "This is a test", "chunk_size": 5}'
```

**2. Stream Metrics:**
```bash
curl -X GET http://localhost:8000/api/v1/stream/metrics \
  -H "X-API-Key: dev-api-key-12345-change-in-production"
```

**3. Stream Analysis:**
```bash
curl -X POST http://localhost:8000/api/v1/stream/analysis \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-12345-change-in-production" \
  -d '{"content": "I love this product!", "analysis_type": "sentiment"}'
```

**All endpoints are listed in the README.md file.**

---

## Step 6: Docker Deployment

Docker packages your application so it runs the same way everywhere.

### 6.1 Build Docker Image

```bash
docker build -t fastapi-streaming:latest .
```

**What this does:**
- Reads the `Dockerfile`
- Creates a Docker image with your application
- Takes 2-5 minutes the first time

**Expected output:** "Successfully built..." and "Successfully tagged..."

### 6.2 Run with Docker Compose

```bash
docker-compose up -d --build
```

**What this does:**
- Builds the Docker image
- Starts the FastAPI container
- Starts the Nginx container (load balancer)
- Runs in background (`-d` flag)

**Expected output:**
```
Creating network "api-app_app-network" ...
Creating fastapi-streaming ...
Creating fastapi-nginx ...
```

### 6.3 Check Running Containers

```bash
docker ps
```

**You should see 2 containers running:**
- `fastapi-streaming`
- `fastapi-nginx`

### 6.4 Test Docker Deployment

```bash
# Test through Nginx (port 80)
curl http://localhost/health

# Or test directly (port 8000)
curl http://localhost:8000/health
```

### 6.5 View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs fastapi
```

### 6.6 Stop Docker Containers

```bash
docker-compose down
```

**This stops and removes the containers.**

---

## Step 7: AWS Account Setup

### 7.1 Create AWS Account

If you don't have an AWS account:

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the signup process
4. **Important:** You'll need a credit card, but we'll use Free Tier resources

### 7.2 Set Up Billing Alerts

**CRITICAL:** Set up billing alerts to avoid unexpected charges!

1. Go to AWS Console → Billing Dashboard
2. Click "Preferences" → Enable "Receive Billing Alerts"
3. Go to CloudWatch → Alarms → Create Alarm
4. Set alarm for:
   - Estimated charges > $10
   - Estimated charges > $25
   - Estimated charges > $50

### 7.3 Create IAM User (Recommended)

For security, create a separate IAM user instead of using root account:

1. Go to IAM → Users → Add Users
2. Username: `fastapi-deploy`
3. Select "Programmatic access"
4. Attach policy: `AdministratorAccess` (for simplicity, or create custom policy)
5. **Save the Access Key ID and Secret Access Key** - you'll need these!

### 7.4 Configure AWS CLI

```bash
aws configure
```

Enter:
- **AWS Access Key ID:** (from Step 7.3)
- **AWS Secret Access Key:** (from Step 7.3)
- **Default region:** `us-east-1`
- **Default output format:** `json`

**Test configuration:**
```bash
aws sts get-caller-identity
```

**Expected output:** Your AWS account ID and user info.

### 7.5 Request GPU Quota (Optional - Only if you need GPU)

If you want GPU support (NOT free tier):

1. Go to AWS Console → Service Quotas
2. Search for "EC2"
3. Request increase for "Running On-Demand G instances"
4. **Note:** This may take 24-48 hours to approve

**For Free Tier testing, skip this step!**

---

## Step 8: AWS Deployment

### 8.1 Set Environment Variables

```bash
# Get your AWS Account ID
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Set region
export AWS_REGION=us-east-1

# Set repository name
export ECR_REPOSITORY=fastapi-streaming

# Set cluster name
export EKS_CLUSTER_NAME=streaming-cluster

# Verify
echo "Account ID: $AWS_ACCOUNT_ID"
echo "Region: $AWS_REGION"
```

### 8.2 Run Automated Deployment Script

**This script does everything automatically!**

```bash
# Make sure script is executable
chmod +x scripts/deploy-aws.sh

# Run the script
./scripts/deploy-aws.sh
```

**What the script does:**
1. Creates ECR repository (Docker image storage)
2. Builds and pushes Docker image
3. Creates EKS cluster (Kubernetes on AWS)
4. Deploys the application
5. Sets up load balancer

**This takes 15-20 minutes!** The EKS cluster creation is the longest step.

### 8.3 Manual Deployment (Alternative)

If the script doesn't work, follow these steps manually:

#### Step 8.3.1: Create ECR Repository

```bash
aws ecr create-repository \
    --repository-name fastapi-streaming \
    --region us-east-1 \
    --image-scanning-configuration scanOnPush=true
```

**Expected output:** Repository details with URI.

#### Step 8.3.2: Authenticate Docker to ECR

```bash
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

**Expected output:** "Login Succeeded"

#### Step 8.3.3: Build and Push Docker Image

```bash
# Build
docker build -t fastapi-streaming:v1 .

# Tag
docker tag fastapi-streaming:v1 $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fastapi-streaming:v1

# Push
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fastapi-streaming:v1
```

**This takes 5-10 minutes** to push the image.

#### Step 8.3.4: Update Kubernetes Deployment File

```bash
# Replace YOUR_ACCOUNT_ID with your actual account ID
sed -i.bak "s|YOUR_ACCOUNT_ID|$AWS_ACCOUNT_ID|g" kubernetes/aws-deployment.yaml
```

#### Step 8.3.5: Create EKS Cluster

**⚠️ IMPORTANT: This costs money (~$0.10/hour for control plane)**

```bash
eksctl create cluster \
    --name streaming-cluster \
    --region us-east-1 \
    --nodegroup-name standard-nodes \
    --node-type t3.micro \
    --nodes 2 \
    --nodes-min 1 \
    --nodes-max 3 \
    --managed
```

**This takes 10-15 minutes!** The cluster is being created.

**Expected output:** "EKS cluster "streaming-cluster" in "us-east-1" region is ready"

#### Step 8.3.6: Update kubeconfig

```bash
aws eks update-kubeconfig --name streaming-cluster --region us-east-1
```

**Test connection:**
```bash
kubectl get nodes
```

**Expected output:** List of nodes (should show 2 nodes).

#### Step 8.3.7: Deploy Application

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Create config
kubectl apply -f kubernetes/configmap.yaml

# Deploy application
kubectl apply -f kubernetes/aws-deployment.yaml

# Create service (load balancer)
kubectl apply -f kubernetes/aws-service.yaml

# Create autoscaler
kubectl apply -f kubernetes/aws-hpa.yaml
```

#### Step 8.3.8: Wait for Deployment

```bash
# Check pod status
kubectl get pods -n fastapi-streaming

# Wait for pods to be ready
kubectl wait --for=condition=available --timeout=300s \
    deployment/fastapi-streaming -n fastapi-streaming
```

**Expected output:** "deployment.apps/fastapi-streaming condition met"

---

## Step 9: Verification & Testing

### 9.1 Check Deployment Status

```bash
# Check pods
kubectl get pods -n fastapi-streaming

# Check services
kubectl get svc -n fastapi-streaming

# Check deployment
kubectl get deployment -n fastapi-streaming
```

**All should show "Running" or "Ready" status.**

### 9.2 Get Load Balancer URL

```bash
# Get the external URL
kubectl get svc fastapi-streaming-service -n fastapi-streaming

# Or get just the URL
kubectl get svc fastapi-streaming-service -n fastapi-streaming \
    -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

**Note:** It may take 2-5 minutes for the LoadBalancer to get an external IP.

**If it shows `<pending>`, wait a few minutes and check again:**
```bash
watch kubectl get svc fastapi-streaming-service -n fastapi-streaming
```

### 9.3 Test the Deployed Application

Once you have the LoadBalancer URL (e.g., `a1b2c3d4e5f6g7h8.us-east-1.elb.amazonaws.com`):

```bash
# Set the URL
export LB_URL=$(kubectl get svc fastapi-streaming-service -n fastapi-streaming \
    -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test health check
curl http://$LB_URL/health

# Test an endpoint
curl -X POST http://$LB_URL/api/v1/stream/text \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-12345-change-in-production" \
  -d '{"text": "Hello from AWS!", "chunk_size": 5}'
```

### 9.4 View Logs

```bash
# View pod logs
kubectl logs -n fastapi-streaming -l app=fastapi-streaming

# Follow logs
kubectl logs -n fastapi-streaming -l app=fastapi-streaming -f

# View logs for specific pod
kubectl logs -n fastapi-streaming <pod-name>
```

### 9.5 Check Resource Usage

```bash
# Check CPU and memory usage
kubectl top pods -n fastapi-streaming

# Check node resources
kubectl top nodes
```

### 9.6 Test Auto-Scaling

The Horizontal Pod Autoscaler (HPA) will automatically scale pods based on load:

```bash
# Check HPA status
kubectl get hpa -n fastapi-streaming

# Describe HPA to see scaling events
kubectl describe hpa fastapi-streaming-hpa -n fastapi-streaming
```

---

## Step 10: Cleanup

**⚠️ IMPORTANT: Delete AWS resources to avoid charges!**

### 10.1 Delete EKS Cluster

```bash
eksctl delete cluster --name streaming-cluster --region us-east-1
```

**This takes 5-10 minutes** and will delete:
- EKS cluster
- EC2 instances
- Load balancer
- All associated resources

### 10.2 Delete ECR Repository

```bash
# Delete all images first
aws ecr list-images --repository-name fastapi-streaming --region us-east-1 \
    --query 'imageIds[*]' --output json | \
    jq -r '.[] | "\(.imageDigest)"' | \
    xargs -I {} aws ecr batch-delete-image \
    --repository-name fastapi-streaming \
    --region us-east-1 \
    --image-ids imageDigest={}

# Delete repository
aws ecr delete-repository \
    --repository-name fastapi-streaming \
    --region us-east-1 \
    --force
```

### 10.3 Verify Cleanup

```bash
# Check for any remaining resources
aws eks list-clusters --region us-east-1
aws ecr describe-repositories --region us-east-1
```

**Should show no resources.**

### 10.4 Stop Local Docker Containers

```bash
docker-compose down
```

---

## Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "Port 8000 already in use"

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
uvicorn app.main:app --reload --port 8001
```

### Problem: "Docker daemon not running"

**Solution:**
- Make sure Docker Desktop is running
- On Mac/Windows: Open Docker Desktop application
- Wait for it to fully start (whale icon in system tray)

### Problem: "AWS credentials not configured"

**Solution:**
```bash
aws configure
# Enter your Access Key ID and Secret Access Key
```

### Problem: "EKS cluster creation failed"

**Solution:**
- Check your AWS account has permissions
- Try a different region: `us-west-2`, `eu-west-1`
- Check if you have service quotas available
- Make sure you have a credit card on file (even for Free Tier)

### Problem: "LoadBalancer stuck in pending"

**Solution:**
- Wait 5-10 minutes (AWS takes time to provision)
- Check your AWS account limits
- Verify you're using a supported region

### Problem: "Pods not starting"

**Solution:**
```bash
# Check pod status
kubectl describe pod <pod-name> -n fastapi-streaming

# Check events
kubectl get events -n fastapi-streaming --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name> -n fastapi-streaming
```

### Problem: "Rate limit exceeded"

**Solution:**
- Wait 1 minute
- The rate limit is 100 requests per minute per IP
- This is by design for the assessment

### Problem: "Invalid API key"

**Solution:**
- Make sure you're using the correct API key
- Check `.env` file or Kubernetes ConfigMap
- Default key: `dev-api-key-12345-change-in-production`

---

## ✅ Completion Checklist

Use this checklist to make sure you've completed everything:

### Local Development
- [ ] Python virtual environment created and activated
- [ ] Dependencies installed
- [ ] Application runs locally
- [ ] All 10 endpoints tested
- [ ] API documentation accessible at /docs

### Docker Deployment
- [ ] Docker image builds successfully
- [ ] Docker Compose starts containers
- [ ] Application accessible through Docker
- [ ] Logs are viewable

### AWS Deployment
- [ ] AWS account created and configured
- [ ] Billing alerts set up
- [ ] ECR repository created
- [ ] Docker image pushed to ECR
- [ ] EKS cluster created
- [ ] Application deployed to Kubernetes
- [ ] LoadBalancer has external IP
- [ ] Application accessible via LoadBalancer URL
- [ ] All endpoints tested on AWS

### Documentation
- [ ] Screenshots taken of:
  - [ ] Local deployment running
  - [ ] Docker containers running
  - [ ] EKS cluster created
  - [ ] Pods running in Kubernetes
  - [ ] LoadBalancer with external IP
  - [ ] API endpoints tested
- [ ] Work summary document filled out

### Cleanup
- [ ] EKS cluster deleted
- [ ] ECR repository deleted
- [ ] Local Docker containers stopped
- [ ] Billing verified (no unexpected charges)

---

## 🎉 Congratulations!

If you've completed all the steps above, you've successfully:

1. ✅ Created a FastAPI application with 10 streaming endpoints
2. ✅ Deployed it locally
3. ✅ Containerized it with Docker
4. ✅ Deployed it to AWS EKS
5. ✅ Tested all functionality
6. ✅ Cleaned up resources

**You're ready to submit your assessment!**

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Docker Docs:** https://docs.docker.com
- **Kubernetes Docs:** https://kubernetes.io/docs
- **AWS EKS Docs:** https://docs.aws.amazon.com/eks
- **AWS Free Tier:** https://aws.amazon.com/free

---

## 💡 Tips for Success

1. **Read error messages carefully** - They usually tell you what's wrong
2. **Check logs** - `docker-compose logs` or `kubectl logs` are your friends
3. **Take screenshots** - Document your progress
4. **Test incrementally** - Don't wait until the end to test
5. **Ask for help** - If stuck, document what you tried and ask

---

## 🆘 Still Need Help?

If you're stuck:

1. Check the error message carefully
2. Review the relevant step in this guide
3. Check the troubleshooting section
4. Review logs (Docker or Kubernetes)
5. Search for the error message online
6. Document what you tried before asking for help

**Good luck with your assessment! 🚀**

