"""
Transcription Streaming Router
"""
import asyncio
from typing import AsyncGenerator

async def generate_transcription_stream(audio_url: str, language: str) -> AsyncGenerator[str, None]:
    """Generate transcription stream"""
    # Simulate streaming transcription
    transcription_parts = [
        "Hello", "world", "this", "is", "a", "streaming", "transcription",
        "of", "the", "audio", "file", "from", audio_url, "in", language, "language."
    ]
    
    for part in transcription_parts:
        yield part + " "
        await asyncio.sleep(0.15)
    
    yield "\n[Transcription complete]"

