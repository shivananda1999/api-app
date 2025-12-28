"""
Text Streaming Router
"""
import asyncio
from typing import AsyncGenerator

async def generate_text_stream(text: str, chunk_size: int) -> AsyncGenerator[str, None]:
    """Generate text stream in chunks"""
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        yield chunk
        await asyncio.sleep(0.1)  # Simulate processing delay

