"""
Logs Streaming Router
"""
import asyncio
from typing import AsyncGenerator
from datetime import datetime
import random

LOG_MESSAGES = {
    "DEBUG": ["Debug: Processing request", "Debug: Cache hit", "Debug: Database query"],
    "INFO": ["Info: User logged in", "Info: Request processed", "Info: Cache updated"],
    "WARNING": ["Warning: High memory usage", "Warning: Slow query detected", "Warning: Rate limit approaching"],
    "ERROR": ["Error: Database connection failed", "Error: Invalid input", "Error: Service unavailable"],
    "CRITICAL": ["Critical: System failure", "Critical: Data corruption", "Critical: Security breach"]
}

async def generate_log_stream(log_level: str, lines: int) -> AsyncGenerator[str, None]:
    """Generate log stream"""
    messages = LOG_MESSAGES.get(log_level, LOG_MESSAGES["INFO"])
    
    for i in range(lines):
        timestamp = datetime.now().isoformat()
        message = random.choice(messages)
        log_line = f"[{timestamp}] {log_level}: {message} - Line {i+1}\n"
        yield log_line
        await asyncio.sleep(0.05)

