import time
import asyncio
from syncit import syncit, is_async_mode


async def async_query():
    await asyncio.sleep(0.1)
    return 5

def query():
    time.sleep(0.1)
    return 5


# Method 1
# Explicit trasnformation

async def f_async():
    if is_async_mode:
        q_result = await async_query()
    else:
        q_result = query()
    return q_result * 2

# get the sync version
f = syncit(f_async)

# Synchronous call
# result = f()

# Asynchronous call
# result = await f_async()


# Method 2
# Inplace transformation using it as a decorator

@syncit
async def g():
    if is_async_mode:
        q_result = await async_query()
    else:
        q_result = query()
    return q_result * 2

# Synchronous call
# result = g()

# Asynchronous call
# result = await g.async_call()
