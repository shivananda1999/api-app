"""
Analysis Streaming Router
"""
import asyncio
import json
from typing import AsyncGenerator

async def generate_analysis_stream(content: str, analysis_type: str) -> AsyncGenerator[str, None]:
    """Generate analysis stream"""
    # Simulate streaming analysis
    if analysis_type == "sentiment":
        results = {
            "sentiment": "positive",
            "confidence": 0.85,
            "scores": {"positive": 0.85, "neutral": 0.10, "negative": 0.05}
        }
    elif analysis_type == "entity":
        results = {
            "entities": [
                {"text": "FastAPI", "type": "TECHNOLOGY", "confidence": 0.95},
                {"text": "streaming", "type": "CONCEPT", "confidence": 0.90}
            ]
        }
    elif analysis_type == "topic":
        results = {
            "topics": ["API", "Streaming", "Technology", "Development"],
            "scores": [0.95, 0.85, 0.75, 0.65]
        }
    else:  # summary
        results = {
            "summary": "This is a summary of the content.",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "length": len(content)
        }
    
    # Stream results in chunks
    result_json = json.dumps(results, indent=2)
    chunk_size = 50
    for i in range(0, len(result_json), chunk_size):
        chunk = result_json[i:i + chunk_size]
        yield chunk
        await asyncio.sleep(0.1)

