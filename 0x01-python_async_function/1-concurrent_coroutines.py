#!/usr/bin/env python3
"""Import wait_random from the previous task and write an async
routine called wait_n that takes in 2 integers: n and max_delay.

wait_n will call wait_random n times and return the list of delays
in ascending order, without using sort().
"""

import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Run wait_random n times and collect the delays."""
    delays = []
    coros = [wait_random(max_delay) for _ in range(n)]

    for coro in asyncio.as_completed(coros):
        delays.append(await coro)

    return sorted(delays)
