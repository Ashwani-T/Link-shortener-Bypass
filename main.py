import asyncio
from bot_handler import create_bot
from worker import queue_worker
from user_client import client
import logging

logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

app = create_bot()

app.bot_data["queue"] = asyncio.Queue()
app.bot_data["request_counter"] = 0
app.bot_data["processed_counter"] = 0

async def post_init(app):
    await client.start()
    asyncio.create_task(queue_worker(app))

app.post_init = post_init

app.run_polling()
