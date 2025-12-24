import asyncio

pending_requests: dict[int, asyncio.Future] = {}
