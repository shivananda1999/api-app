#!/bin/bash

# API Testing Script
# Tests all 10 endpoints of the FastAPI streaming application

set -e

BASE_URL=${BASE_URL:-http://localhost:8000}
API_KEY=${API_KEY:-dev-api-key-12345-change-in-production}

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Testing FastAPI Streaming Application${NC}"
echo "Base URL: $BASE_URL"
echo ""

# Test Health Check
echo -e "${YELLOW}1. Testing Health Check...${NC}"
curl -s "$BASE_URL/health" | jq . || echo "Health check failed"
echo ""

# Test Endpoint 1: Stream Text
echo -e "${YELLOW}2. Testing Stream Text...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/text" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"text": "Hello World, this is a test", "chunk_size": 5}' \
  | head -c 100
echo ""
echo ""

# Test Endpoint 2: Stream Audio
echo -e "${YELLOW}3. Testing Stream Audio...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/audio" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"audio_url": "https://example.com/audio.wav", "sample_rate": 44100}' \
  | head -c 100
echo ""
echo ""

# Test Endpoint 3: Stream Video
echo -e "${YELLOW}4. Testing Stream Video...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/video" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"video_url": "https://example.com/video.mp4", "fps": 30}' \
  | head -c 100
echo ""
echo ""

# Test Endpoint 4: Stream Data
echo -e "${YELLOW}5. Testing Stream Data...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/data" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"data": {"key1": "value1", "key2": "value2"}, "format": "json"}' \
  | head -c 200
echo ""
echo ""

# Test Endpoint 5: Stream Logs
echo -e "${YELLOW}6. Testing Stream Logs...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/logs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"log_level": "INFO", "lines": 10}' \
  | head -c 500
echo ""
echo ""

# Test Endpoint 6: Stream Metrics
echo -e "${YELLOW}7. Testing Stream Metrics...${NC}"
curl -s -X GET "$BASE_URL/api/v1/stream/metrics" \
  -H "X-API-Key: $API_KEY" \
  | head -c 200
echo ""
echo ""

# Test Endpoint 7: Stream Chat
echo -e "${YELLOW}8. Testing Stream Chat...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"message": "Hello, how are you?", "model": "gpt-3.5-turbo"}' \
  | head -c 200
echo ""
echo ""

# Test Endpoint 8: Stream Transcription
echo -e "${YELLOW}9. Testing Stream Transcription...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/transcription" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"audio_url": "https://example.com/audio.wav", "language": "en"}' \
  | head -c 200
echo ""
echo ""

# Test Endpoint 9: Stream Translation
echo -e "${YELLOW}10. Testing Stream Translation...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/translation" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"text": "Hello, world!", "source_lang": "en", "target_lang": "es"}' \
  | head -c 200
echo ""
echo ""

# Test Endpoint 10: Stream Analysis
echo -e "${YELLOW}11. Testing Stream Analysis...${NC}"
curl -s -X POST "$BASE_URL/api/v1/stream/analysis" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"content": "This is a positive review", "analysis_type": "sentiment"}' \
  | head -c 300
echo ""
echo ""

echo -e "${GREEN}All tests completed!${NC}"

