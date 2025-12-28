"""
Data Streaming Router
"""
import asyncio
import json
from typing import AsyncGenerator, Dict, Any

async def generate_data_stream(data: Dict[str, Any], format: str) -> AsyncGenerator[str, None]:
    """Generate structured data stream"""
    if format == "json":
        # Stream data as JSON chunks
        items = list(data.items())
        for key, value in items:
            chunk = json.dumps({key: value}) + "\n"
            yield chunk
            await asyncio.sleep(0.1)
    elif format == "csv":
        # Stream as CSV
        headers = ",".join(data.keys()) + "\n"
        yield headers
        values = ",".join(str(v) for v in data.values()) + "\n"
        yield values
    else:  # xml
        # Stream as XML
        for key, value in data.items():
            chunk = f"<{key}>{value}</{key}>\n"
            yield chunk
            await asyncio.sleep(0.1)

