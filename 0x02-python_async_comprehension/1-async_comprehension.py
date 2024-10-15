#!/usr/bin/env python3
'''Task 1: Async Comprehensions
Import async_generator from the previous task and then write
a coroutine called async_comprehension that takes no arguments.

The coroutine will collect 10 random numbers using an async
comprehension over async_generator, then return the 10 random
numbers.
'''

from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    '''Collects and returns 10 random numbers from the async generator.
    '''
    return [value async for value in async_generator()]
