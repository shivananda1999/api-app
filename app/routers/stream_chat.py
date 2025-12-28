"""
Chat Streaming Router
"""
import asyncio
from typing import AsyncGenerator

async def generate_chat_stream(message: str, model: str) -> AsyncGenerator[str, None]:
    """Generate chat response stream"""
    # Simulate streaming chat response
    response_words = [
        "This", "is", "a", "streaming", "chat", "response", "generated", 
        "by", "the", model, "model.", "The", "message", "you", "sent", 
        "was:", message[:50], "..."
    ]
    
    for word in response_words:
        chunk = f"data: {word} \n\n"
        yield chunk
        await asyncio.sleep(0.2)
    
    yield "data: [DONE]\n\n"

