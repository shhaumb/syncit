import time
import asyncio
from syncit import syncit, is_async_mode


async def async_query():
    await asyncio.sleep(0.1)
    return 5

def query():
    time.sleep(0.1)
    return 5


async def f_async():
    if is_async_mode:
        result = await async_query()
    else:
        result = query()
    return result * 2

f = syncit(f_async)
