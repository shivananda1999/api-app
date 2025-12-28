"""
Audio Streaming Router
"""
import asyncio
from typing import AsyncGenerator
import base64

async def generate_audio_stream(audio_url: str, sample_rate: int) -> AsyncGenerator[bytes, None]:
    """Generate audio stream in chunks"""
    # Simulate audio streaming
    chunk_size = 1024
    total_chunks = 100
    
    for i in range(total_chunks):
        # Simulate audio data chunk
        audio_data = b'\x00' * chunk_size
        yield audio_data
        await asyncio.sleep(0.01)

