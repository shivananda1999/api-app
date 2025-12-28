# Quick Start Guide

> **👋 New to this project?** Start with [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) for a complete step-by-step walkthrough!

## 🚀 Fastest Way to Get Started

### Option 1: Local Development (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
echo "API_KEY=dev-api-key-12345-change-in-production" > .env

# 3. Run the application
uvicorn app.main:app --reload

# 4. Test it
curl http://localhost:8000/health
```

### Option 2: Docker (2 minutes)

```bash
# 1. Build and run
docker-compose up -d --build

# 2. Test it
curl http://localhost:8000/health

# 3. View logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

### Option 3: AWS EKS (15-20 minutes)

```bash
# 1. Set your AWS credentials
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 2. Run deployment script
./scripts/deploy-aws.sh

# 3. Wait for LoadBalancer (2-5 minutes)
kubectl get svc -n fastapi-streaming -w

# 4. Get the URL and test
EXTERNAL_IP=$(kubectl get svc fastapi-streaming-service -n fastapi-streaming -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl http://$EXTERNAL_IP/health
```

## 📝 Testing All Endpoints

```bash
# Run the test script
./scripts/test-api.sh

# Or test manually
curl -X POST http://localhost:8000/api/v1/stream/text \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-12345-change-in-production" \
  -d '{"text": "Hello World", "chunk_size": 5}'
```

## 🔑 API Key

Default API key for development:
```
dev-api-key-12345-change-in-production
```

Change it in `.env` file or Kubernetes ConfigMap for production.

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [WORK_SUMMARY.md](WORK_SUMMARY.md) for assessment template
3. Visit http://localhost:8000/docs for interactive API documentation

## ⚠️ Important Notes

- **Free Tier**: Use `t3.micro` instances on AWS (Free Tier eligible)
- **Costs**: EKS control plane costs ~$0.10/hour (~$72/month)
- **Cleanup**: Always delete AWS resources after testing!
- **GPU**: GPU instances are NOT in Free Tier, use only if you have budget

## 🆘 Need Help?

1. Check [README.md](README.md) troubleshooting section
2. View logs: `docker-compose logs` or `kubectl logs -n fastapi-streaming`
3. Check health: `curl http://localhost:8000/health`

