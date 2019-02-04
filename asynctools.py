import asyncio


async def wait_cancel(coro, timeout):
    task = asyncio.ensure_future(coro)
    try:
        res = await asyncio.wait_for(task, timeout=timeout)
        return res, False
    except asyncio.TimeoutError as e:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError as e:
            pass
        return None, True


def test_wait_cancel():
    counter = 0

    async def _sleeper():
        nonlocal counter
        while True:
            counter += 1
            await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_cancel(_sleeper(), 5))
    assert counter >= 4

    counter = 0
    loop.run_until_complete(wait_cancel(_sleeper(), 3))
    assert counter <= 3


if __name__ == "__main__":
    test_wait_cancel()
