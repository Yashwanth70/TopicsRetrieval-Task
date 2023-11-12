import asyncio


def schedule(func, args=None, kwargs=None, interval=60, *, loop):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    async def periodic_func():
        while True:
            await asyncio.sleep(interval, loop=loop)
            await func(*args, **kwargs)
    return loop.create_task(periodic_func())