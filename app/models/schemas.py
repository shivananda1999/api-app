"""
Pydantic Models for Request Validation
"""
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum

class StreamTextRequest(BaseModel):
    text: str = Field(..., description="Text content to stream", min_length=1)
    chunk_size: int = Field(default=10, description="Characters per chunk", ge=1, le=1000)

class StreamAudioRequest(BaseModel):
    audio_url: HttpUrl = Field(..., description="URL of audio file to stream")
    sample_rate: int = Field(default=44100, description="Audio sample rate", ge=8000, le=192000)

class StreamVideoRequest(BaseModel):
    video_url: HttpUrl = Field(..., description="URL of video file to stream")
    fps: int = Field(default=30, description="Frames per second", ge=1, le=120)

class StreamDataRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="Data to stream")
    format: str = Field(default="json", description="Output format")
    
    @field_validator('format')
    @classmethod
    def validate_format(cls, v):
        if v not in ['json', 'csv', 'xml']:
            raise ValueError('format must be json, csv, or xml')
        return v

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StreamLogsRequest(BaseModel):
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Log level filter")
    lines: int = Field(default=100, description="Number of log lines", ge=1, le=10000)

class StreamMetricsRequest(BaseModel):
    interval: int = Field(default=1, description="Metrics update interval in seconds", ge=1, le=60)

class StreamChatRequest(BaseModel):
    message: str = Field(..., description="Chat message", min_length=1)
    model: str = Field(default="gpt-3.5-turbo", description="Model to use for chat")

class StreamTranscriptionRequest(BaseModel):
    audio_url: HttpUrl = Field(..., description="URL of audio file to transcribe")
    language: str = Field(default="en", description="Language code (ISO 639-1)", min_length=2, max_length=5)

class StreamTranslationRequest(BaseModel):
    text: str = Field(..., description="Text to translate", min_length=1)
    source_lang: str = Field(default="en", description="Source language code", min_length=2, max_length=5)
    target_lang: str = Field(..., description="Target language code", min_length=2, max_length=5)

class AnalysisType(str, Enum):
    SENTIMENT = "sentiment"
    ENTITY = "entity"
    TOPIC = "topic"
    SUMMARY = "summary"

class StreamAnalysisRequest(BaseModel):
    content: str = Field(..., description="Content to analyze", min_length=1)
    analysis_type: AnalysisType = Field(..., description="Type of analysis to perform")

