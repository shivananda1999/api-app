"""
FastAPI Streaming Application
Main application entry point with 10 streaming endpoints
"""
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import time
import json
import asyncio
from typing import Optional, List
import os
from dotenv import load_dotenv

from app.routers import (
    stream_text,
    stream_audio,
    stream_video,
    stream_data,
    stream_logs,
    stream_metrics,
    stream_chat,
    stream_transcription,
    stream_translation,
    stream_analysis
)
from app.middleware.auth import verify_api_key
from app.models.schemas import (
    StreamTextRequest,
    StreamAudioRequest,
    StreamVideoRequest,
    StreamDataRequest,
    StreamLogsRequest,
    StreamMetricsRequest,
    StreamChatRequest,
    StreamTranscriptionRequest,
    StreamTranslationRequest,
    StreamAnalysisRequest
)

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Streaming Application",
    description="GPU-accelerated streaming API with 10 endpoints",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fastapi-streaming"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FastAPI Streaming Application",
        "version": "1.0.0",
        "endpoints": 10,
        "docs": "/docs"
    }

# Endpoint 1: Stream Text
@app.post("/api/v1/stream/text")
@limiter.limit("100/minute")
async def stream_text_endpoint(
    request_data: StreamTextRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream text content in chunks"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_text.generate_text_stream(request_data.text, request_data.chunk_size),
        media_type="text/plain"
    )

# Endpoint 2: Stream Audio
@app.post("/api/v1/stream/audio")
@limiter.limit("100/minute")
async def stream_audio_endpoint(
    request_data: StreamAudioRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream audio data in chunks"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_audio.generate_audio_stream(request_data.audio_url, request_data.sample_rate),
        media_type="audio/wav"
    )

# Endpoint 3: Stream Video
@app.post("/api/v1/stream/video")
@limiter.limit("100/minute")
async def stream_video_endpoint(
    request_data: StreamVideoRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream video frames"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_video.generate_video_stream(request_data.video_url, request_data.fps),
        media_type="video/mp4"
    )

# Endpoint 4: Stream Data
@app.post("/api/v1/stream/data")
@limiter.limit("100/minute")
async def stream_data_endpoint(
    request_data: StreamDataRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream structured data"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_data.generate_data_stream(request_data.data, request_data.format),
        media_type="application/json"
    )

# Endpoint 5: Stream Logs
@app.post("/api/v1/stream/logs")
@limiter.limit("100/minute")
async def stream_logs_endpoint(
    request_data: StreamLogsRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream application logs"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_logs.generate_log_stream(request_data.log_level, request_data.lines),
        media_type="text/plain"
    )

# Endpoint 6: Stream Metrics
@app.get("/api/v1/stream/metrics")
@limiter.limit("100/minute")
async def stream_metrics_endpoint(
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream system and application metrics"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_metrics.generate_metrics_stream(),
        media_type="application/json"
    )

# Endpoint 7: Stream Chat
@app.post("/api/v1/stream/chat")
@limiter.limit("100/minute")
async def stream_chat_endpoint(
    request_data: StreamChatRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream chat responses"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_chat.generate_chat_stream(request_data.message, request_data.model),
        media_type="text/event-stream"
    )

# Endpoint 8: Stream Transcription
@app.post("/api/v1/stream/transcription")
@limiter.limit("100/minute")
async def stream_transcription_endpoint(
    request_data: StreamTranscriptionRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream audio transcription"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_transcription.generate_transcription_stream(
            request_data.audio_url, request_data.language
        ),
        media_type="text/plain"
    )

# Endpoint 9: Stream Translation
@app.post("/api/v1/stream/translation")
@limiter.limit("100/minute")
async def stream_translation_endpoint(
    request_data: StreamTranslationRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream translation results"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_translation.generate_translation_stream(
            request_data.text, request_data.source_lang, request_data.target_lang
        ),
        media_type="text/plain"
    )

# Endpoint 10: Stream Analysis
@app.post("/api/v1/stream/analysis")
@limiter.limit("100/minute")
async def stream_analysis_endpoint(
    request_data: StreamAnalysisRequest,
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Stream analysis results"""
    await verify_api_key(api_key)
    return StreamingResponse(
        stream_analysis.generate_analysis_stream(
            request_data.content, request_data.analysis_type
        ),
        media_type="application/json"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

