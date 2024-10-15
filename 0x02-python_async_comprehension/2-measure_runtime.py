#!/usr/bin/env python3
'''Task 2: Run time for four parallel comprehensions
'''

import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''Runs async_comprehension 4 times concurrently and calculates
    the total time taken for execution.
    '''
    start = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    return time.perf_counter() - start
