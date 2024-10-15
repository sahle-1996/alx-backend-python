#!/usr/bin/env python3
"""Import wait_random from 0-basic_async_syntax.

Define a function task_wait_random that takes an integer max_delay
and returns an asyncio.Task.
"""

import asyncio
from typing import Any
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> Any:
    """Creates and returns an asyncio.Task for wait_random."""
    return asyncio.ensure_future(wait_random(max_delay))
