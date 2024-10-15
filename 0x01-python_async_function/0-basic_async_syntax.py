#!/usr/bin/env python3
"""Async function that waits for a random delay up to max_delay seconds
and then returns the delay time.
"""

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """Pause for a random amount of time and return the delay"""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
