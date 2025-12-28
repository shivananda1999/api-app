"""
Video Streaming Router
"""
import asyncio
from typing import AsyncGenerator

async def generate_video_stream(video_url: str, fps: int) -> AsyncGenerator[bytes, None]:
    """Generate video stream frame by frame"""
    frame_delay = 1.0 / fps
    total_frames = 300  # 10 seconds at 30fps
    
    for i in range(total_frames):
        # Simulate video frame data
        frame_data = b'\x00' * 10240  # 10KB per frame
        yield frame_data
        await asyncio.sleep(frame_delay)

