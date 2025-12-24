import asyncio

request_counter = 0
processed_counter = 0
lock = asyncio.Lock()
