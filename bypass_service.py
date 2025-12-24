import re
import os
from dotenv import load_dotenv
import asyncio
from telethon import events
from user_client import client
from request_registry import pending_requests
load_dotenv()

TARGET_BOT = os.getenv("TARGET_BOT_TOKEN")

SUCCESS_REGEX = r"Bypassed Link\s*:\s*(https?://[^\s]+)"
ERROR_REGEX = r"Error\s*:-\s*(.+)"

@client.on(events.NewMessage(from_users=TARGET_BOT))
async def handle_bypass_reply(event):
    if not event.reply_to_msg_id:
        return

    future = pending_requests.get(event.reply_to_msg_id)
    if not future or future.done():
        return

    text = event.raw_text or ""

    #  SUCCESS
    success_match = re.search(SUCCESS_REGEX, text)
    if success_match:
        future.set_result(("success", success_match.group(1)))
        del pending_requests[event.reply_to_msg_id]
        return

    # KNOWN ERROR
    error_match = re.search(ERROR_REGEX, text)
    if error_match:
        future.set_result(("error", error_match.group(1).strip()))
        del pending_requests[event.reply_to_msg_id]
        return


async def bypass_url(short_url: str, timeout: int = 90):
    if not client.is_connected():
        await client.connect()

    loop = asyncio.get_running_loop()
    future = loop.create_future()

    sent_msg = await client.send_message(TARGET_BOT, "/b "+short_url)
    pending_requests[sent_msg.id] = future

    try:
        return await asyncio.wait_for(future, timeout)
    except asyncio.TimeoutError:
        pending_requests.pop(sent_msg.id, None)
        return None
