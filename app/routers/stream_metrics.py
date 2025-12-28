"""
Metrics Streaming Router
"""
import asyncio
import json
from typing import AsyncGenerator
import random
from datetime import datetime

async def generate_metrics_stream() -> AsyncGenerator[str, None]:
    """Generate system metrics stream"""
    while True:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": round(random.uniform(10, 90), 2),
            "memory_usage": round(random.uniform(20, 80), 2),
            "gpu_usage": round(random.uniform(0, 100), 2),
            "gpu_memory": round(random.uniform(0, 100), 2),
            "requests_per_second": random.randint(10, 100),
            "active_connections": random.randint(5, 50),
            "disk_usage": round(random.uniform(30, 70), 2)
        }
        yield json.dumps(metrics) + "\n"
        await asyncio.sleep(1)

