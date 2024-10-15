#!/usr/bin/env python3
"""Import wait_n from the previous task and define a function
to measure the average runtime of wait_n.
"""

import time
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Calculate the average runtime of wait_n."""
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    duration = time.perf_counter() - start

    return duration / n
