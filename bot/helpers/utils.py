import asyncio
import functools
import threading

def new_task(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(func(*args, **kwargs))
    return wrapper

def run_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper
