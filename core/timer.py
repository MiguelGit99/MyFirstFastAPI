import time
from fastapi import Request

async def timing_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    duration = end_time - start_time
    response.headers["X-Process-Time"] = str(duration)
    return response